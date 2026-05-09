import faulthandler
faulthandler.enable()
import os
import sys

# Set critical environment variables before any heavy imports
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import streamlit as st
import traceback

import cv2 as cv
import numpy as np
import mediapipe as mp
from collections import deque, Counter
import copy
import csv
import av

from streamlit_webrtc import webrtc_streamer, RTCConfiguration, WebRtcMode

from model import KeyPointClassifier, PointHistoryClassifier
from app import (
    calc_bounding_rect,
    calc_landmark_list,
    pre_process_landmark,
    pre_process_point_history,
    draw_bounding_rect,
    draw_landmarks,
    draw_info_text,
    draw_point_history
)

# Initialize Streamlit Page
st.set_page_config(page_title="Hand Gesture Recognition", layout="wide", page_icon="🖖")

page_style = """
<style>
body {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}
.css-18e3th9 {
    background-color: transparent;
}
.css-1outpf7 {
    background-color: rgba(15, 23, 42, 0.92);
    border: 1px solid rgba(148, 163, 184, 0.16);
    box-shadow: 0 20px 60px rgba(15, 23, 42, 0.35);
}
.section-heading h1 {
    margin-bottom: 0.25rem;
    color: #f8fafc;
}
.section-heading p {
    margin-top: 0;
    color: #cbd5e1;
    font-size: 1.05rem;
}
.card {
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 18px;
    padding: 1.35rem;
    box-shadow: 0 16px 40px rgba(15, 23, 42, 0.25);
}
.card h3 {
    color: #f8fafc;
    margin-bottom: 0.75rem;
}
.card p {
    color: #cbd5e1;
    margin: 0;
}
.footer {
    position: fixed;
    left: 1rem;
    bottom: 1rem;
    color: #94a3b8;
    font-size: 0.9rem;
    z-index: 999;
}
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

st.markdown(
    """
<div class='section-heading'>
  <h1>Hand Gesture Recognition Web App</h1>
  <p>Real-time hand sign and finger gesture detection directly from your webcam with a polished browser UI.</p>
</div>
""",
    unsafe_allow_html=True,
)

intro_col1, intro_col2 = st.columns([3, 1])
with intro_col1:
    st.markdown(
        """
        <div class='card'>
            <h3>Overview</h3>
            <p>Capture webcam video, detect hand landmarks using MediaPipe, and classify gestures in real-time with a lightweight model.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with intro_col2:
    st.markdown(
        """
        <div class='card'>
            <h3>Built for Deployment</h3>
            <p>Designed to run in the browser with minimal latency and a clean user experience.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Load Models
@st.cache_resource
def load_models():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1, # simplified to 1 hand for better web performance
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    )
    keypoint_classifier = KeyPointClassifier()
    point_history_classifier = PointHistoryClassifier()
    
    with open('model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
        keypoint_classifier_labels = [row[0] for row in csv.reader(f)]
    with open('model/point_history_classifier/point_history_classifier_label.csv', encoding='utf-8-sig') as f:
        point_history_classifier_labels = [row[0] for row in csv.reader(f)]
        
    return hands, keypoint_classifier, point_history_classifier, keypoint_classifier_labels, point_history_classifier_labels

hands, keypoint_classifier, point_history_classifier, keypoint_classifier_labels, point_history_classifier_labels = load_models()

# State variables for tracking
history_length = 16

class HandGestureProcessor:
    def __init__(self):
        self.point_history = deque(maxlen=history_length)
        self.finger_gesture_history = deque(maxlen=history_length)

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        image = frame.to_ndarray(format="bgr24")
        image = cv.flip(image, 1)  # Mirror display
        debug_image = copy.deepcopy(image)

        image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = hands.process(image_rgb)
        image_rgb.flags.writeable = True

        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                brect = calc_bounding_rect(debug_image, hand_landmarks)
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                pre_processed_landmark_list = pre_process_landmark(landmark_list)
                pre_processed_point_history_list = pre_process_point_history(debug_image, self.point_history)

                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                if hand_sign_id == 2:  # Point gesture
                    self.point_history.append(landmark_list[8])
                else:
                    self.point_history.append([0, 0])

                finger_gesture_id = 0
                if len(pre_processed_point_history_list) == (history_length * 2):
                    finger_gesture_id = point_history_classifier(pre_processed_point_history_list)

                self.finger_gesture_history.append(finger_gesture_id)
                most_common_fg_id = Counter(self.finger_gesture_history).most_common()

                debug_image = draw_bounding_rect(True, debug_image, brect)
                debug_image = draw_landmarks(debug_image, landmark_list)
                debug_image = draw_info_text(
                    debug_image, brect, handedness,
                    keypoint_classifier_labels[hand_sign_id],
                    point_history_classifier_labels[most_common_fg_id[0][0]],
                )
        else:
            self.point_history.append([0, 0])

        debug_image = draw_point_history(debug_image, self.point_history)

        return av.VideoFrame.from_ndarray(debug_image, format="bgr24")

# Streamlit WebRTC Component
st.markdown("### Live Webcam Feed")
st.markdown("Please grant webcam permissions when prompted. It might take a few seconds for the models to load.")

processor = HandGestureProcessor()

webrtc_streamer(
    key="hand-gesture",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=processor.recv,
    rtc_configuration=RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    ),
    media_stream_constraints={"video": True, "audio": False},
)

st.markdown("---")

st.markdown(
    """
    <div class='card'>
        <h3>How to use</h3>
        <ul>
            <li>Allow webcam access and show your hand to the camera.</li>
            <li>The app recognizes static signs such as Open Hand, Close Hand, and Pointing.</li>
            <li>It also tracks finger motion and detects dynamic gestures like Clockwise and Counterclockwise.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="footer">Created by Gururamdas T P</div>', unsafe_allow_html=True)
