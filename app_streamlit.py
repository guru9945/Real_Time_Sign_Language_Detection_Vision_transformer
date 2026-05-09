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
st.set_page_config(page_title="Hand Gesture Recognition", layout="wide")
st.title("Hand Gesture Recognition Web App 🖖")

st.markdown("""
This web app recognizes hand signs and finger gestures in real-time directly from your webcam.
It uses **MediaPipe** for hand tracking and a custom Neural Network for gesture classification.
""")

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
**How to use:**
- Show your hand to the camera.
- The app recognizes static signs like Open Hand, Close Hand, and Pointing.
- It also traces your index finger's path and recognizes dynamic gestures like Clockwise or Counterclockwise motion.
"""
)
