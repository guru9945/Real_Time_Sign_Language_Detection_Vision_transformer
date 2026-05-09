#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hand Gesture Recognition GUI Application
Professional interface for real-time hand gesture recognition
"""

import tkinter as tk
from tkinter import ttk, messagebox
import cv2 as cv
import numpy as np
import mediapipe as mp
import threading
import csv
from collections import deque, Counter
from datetime import datetime
import copy
import itertools
from PIL import Image, ImageTk

from utils import CvFpsCalc
from model import KeyPointClassifier, PointHistoryClassifier


class GestureRecognitionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Gesture Recognition System")
        self.root.geometry("1400x900")
        self.root.config(bg="#f0f0f0")
        
        # Initialize variables
        self.running = False
        self.cap = None
        self.camera_thread = None
        self.mode = 0  # 0: Normal, 1: Keypoint collection, 2: Gesture collection
        self.number = -1
        
        # History and statistics
        self.gesture_history = deque(maxlen=20)
        self.confidence_history = deque(maxlen=20)
        self.fps_history = deque(maxlen=100)
        self.collected_samples = {"keypoint": 0, "gesture": 0}
        
        # Initialize MediaPipe and models
        self.init_models()
        
        # FPS calculator
        self.cvFpsCalc = CvFpsCalc(buffer_len=10)
        
        # Point history
        self.history_length = 16
        self.point_history = deque(maxlen=self.history_length)
        self.finger_gesture_history = deque(maxlen=self.history_length)
        
        # Create GUI
        self.create_widgets()
        
    def init_models(self):
        """Initialize MediaPipe and classifiers"""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )
        
        self.keypoint_classifier = KeyPointClassifier()
        self.point_history_classifier = PointHistoryClassifier()
        
        # Load labels
        with open('model/keypoint_classifier/keypoint_classifier_label.csv',
                  encoding='utf-8-sig') as f:
            self.keypoint_labels = [row[0] for row in csv.reader(f)]
        
        with open('model/point_history_classifier/point_history_classifier_label.csv',
                  encoding='utf-8-sig') as f:
            self.gesture_labels = [row[0] for row in csv.reader(f)]
    
    def create_widgets(self):
        """Create GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Video display
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Video label
        ttk.Label(left_frame, text="Live Feed", font=("Arial", 14, "bold")).pack()
        self.video_label = ttk.Label(left_frame, background="black", relief=tk.SUNKEN)
        self.video_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right panel - Controls and information
        right_frame = ttk.Frame(main_frame, width=350)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # === Control Panel ===
        control_frame = ttk.LabelFrame(right_frame, text="Control Panel", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Start/Stop button
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.start_btn = ttk.Button(button_frame, text="▶ Start Camera", 
                                    command=self.start_camera, width=15)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="⏹ Stop Camera", 
                                   command=self.stop_camera, width=15, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Mode selection
        ttk.Label(control_frame, text="Mode:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        
        self.mode_var = tk.StringVar(value="normal")
        mode_frame = ttk.Frame(control_frame)
        mode_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(mode_frame, text="Normal", variable=self.mode_var, 
                        value="normal", command=self.set_mode_normal).pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Collect Gestures (0-9)", variable=self.mode_var, 
                        value="keypoint", command=self.set_mode_keypoint).pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Collect Finger Gestures (0-9)", variable=self.mode_var, 
                        value="gesture", command=self.set_mode_gesture).pack(anchor=tk.W)
        
        # === Real-time Statistics ===
        stats_frame = ttk.LabelFrame(right_frame, text="Real-time Statistics", padding=10)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # FPS
        fps_frame = ttk.Frame(stats_frame)
        fps_frame.pack(fill=tk.X, pady=5)
        ttk.Label(fps_frame, text="FPS:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.fps_label = ttk.Label(fps_frame, text="--", font=("Arial", 9))
        self.fps_label.pack(side=tk.LEFT, padx=10)
        
        # Hand Sign
        sign_frame = ttk.Frame(stats_frame)
        sign_frame.pack(fill=tk.X, pady=5)
        ttk.Label(sign_frame, text="Hand Sign:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.sign_label = tk.Label(sign_frame, text="--", font=("Arial", 9), foreground="blue", bg="#f0f0f0")
        self.sign_label.pack(side=tk.LEFT, padx=10)
        
        # Gesture
        gesture_frame = ttk.Frame(stats_frame)
        gesture_frame.pack(fill=tk.X, pady=5)
        ttk.Label(gesture_frame, text="Gesture:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.gesture_label = tk.Label(gesture_frame, text="--", font=("Arial", 9), foreground="green", bg="#f0f0f0")
        self.gesture_label.pack(side=tk.LEFT, padx=10)
        
        # Confidence
        conf_frame = ttk.Frame(stats_frame)
        conf_frame.pack(fill=tk.X, pady=5)
        ttk.Label(conf_frame, text="Confidence:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.conf_label = ttk.Label(conf_frame, text="--", font=("Arial", 9))
        self.conf_label.pack(side=tk.LEFT, padx=10)
        
        # === Gesture History ===
        history_frame = ttk.LabelFrame(right_frame, text="Gesture History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Listbox with scrollbar
        scrollbar = ttk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, 
                                          font=("Arial", 8), height=8)
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # === Data Collection Stats ===
        data_frame = ttk.LabelFrame(right_frame, text="Data Collection", padding=10)
        data_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Keypoint samples
        kp_frame = ttk.Frame(data_frame)
        kp_frame.pack(fill=tk.X, pady=3)
        ttk.Label(kp_frame, text="Hand Gestures:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.kp_count_label = tk.Label(kp_frame, text="0", font=("Arial", 9), foreground="blue", bg="white")
        self.kp_count_label.pack(side=tk.LEFT, padx=10)
        
        # Gesture samples
        gesture_cnt_frame = ttk.Frame(data_frame)
        gesture_cnt_frame.pack(fill=tk.X, pady=3)
        ttk.Label(gesture_cnt_frame, text="Finger Gestures:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.gesture_count_label = tk.Label(gesture_cnt_frame, text="0", font=("Arial", 9), foreground="green", bg="white")
        self.gesture_count_label.pack(side=tk.LEFT, padx=10)
        
        # === Project Information ===
        info_frame = ttk.LabelFrame(right_frame, text="Project Info", padding=10)
        info_frame.pack(fill=tk.X)
        
        info_text = """Hand Gesture Recognition
        
✓ Real-time detection
✓ 21 hand landmarks
✓ 5 Hand signs
✓ 4 Finger gestures
✓ MediaPipe + TFLite
        """
        ttk.Label(info_frame, text=info_text, font=("Arial", 8), justify=tk.LEFT).pack()
    
    def set_mode_normal(self):
        self.mode = 0
    
    def set_mode_keypoint(self):
        self.mode = 1
    
    def set_mode_gesture(self):
        self.mode = 2
    
    def start_camera(self):
        """Start camera and gesture recognition"""
        if self.running:
            return
        
        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 960)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 540)
        
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Cannot open camera")
            return
        
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.camera_thread.start()
    
    def stop_camera(self):
        """Stop camera and gesture recognition"""
        self.running = False
        if self.cap:
            self.cap.release()
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.video_label.config(image="")
        self.video_label.image = None
    
    def camera_loop(self):
        """Main camera processing loop"""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            fps = self.cvFpsCalc.get()
            self.fps_history.append(fps)
            
            # Mirror display
            frame = cv.flip(frame, 1)
            debug_image = copy.deepcopy(frame)
            
            # Convert to RGB
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            frame_rgb.flags.writeable = False
            results = self.hands.process(frame_rgb)
            frame_rgb.flags.writeable = True
            
            hand_sign_name = "--"
            gesture_name = "--"
            current_confidence = "--"
            
            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                      results.multi_handedness):
                    # Get landmarks
                    landmark_list = self.calc_landmark_list(debug_image, hand_landmarks)
                    pre_processed_landmark_list = self.pre_process_landmark(landmark_list)
                    pre_processed_point_history_list = self.pre_process_point_history(
                        debug_image, self.point_history)
                    
                    # Log data if in collection mode
                    self.logging_csv(self.number, self.mode, pre_processed_landmark_list,
                                   pre_processed_point_history_list)
                    
                    # Classify hand sign
                    hand_sign_id = self.keypoint_classifier(pre_processed_landmark_list)
                    hand_sign_name = self.keypoint_labels[hand_sign_id]
                    
                    if hand_sign_id == 2:  # Pointer
                        self.point_history.append(landmark_list[8])
                    else:
                        self.point_history.append([0, 0])
                    
                    # Classify gesture
                    finger_gesture_id = 0
                    point_history_len = len(pre_processed_point_history_list)
                    if point_history_len == (self.history_length * 2):
                        finger_gesture_id = self.point_history_classifier(
                            pre_processed_point_history_list)
                    
                    self.finger_gesture_history.append(finger_gesture_id)
                    most_common_fg_id = Counter(self.finger_gesture_history).most_common()
                    
                    if most_common_fg_id:
                        gesture_name = self.gesture_labels[most_common_fg_id[0][0]]
                    
                    # Draw
                    brect = self.calc_bounding_rect(debug_image, hand_landmarks)
                    debug_image = self.draw_bounding_rect(debug_image, brect)
                    debug_image = self.draw_landmarks(debug_image, landmark_list)
                    debug_image = self.draw_info_text(debug_image, brect, handedness,
                                                     hand_sign_name, gesture_name)
            else:
                self.point_history.append([0, 0])
            
            # Draw point history
            debug_image = self.draw_point_history(debug_image, self.point_history)
            debug_image = self.draw_info(debug_image, fps, self.mode, self.number)
            
            # Update gesture history
            if hand_sign_name != "--":
                timestamp = datetime.now().strftime("%H:%M:%S")
                entry = f"[{timestamp}] {hand_sign_name}"
                if gesture_name != "--":
                    entry += f" - {gesture_name}"
                self.gesture_history.append(entry)
            
            # Update UI
            self.update_ui(debug_image, fps, hand_sign_name, gesture_name, current_confidence)
    
    def update_ui(self, frame, fps, hand_sign, gesture, confidence):
        """Update GUI with frame and statistics"""
        # Convert frame to PhotoImage
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_pil = frame_pil.resize((640, 480), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(frame_pil)
        
        self.video_label.config(image=photo)
        self.video_label.image = photo
        
        # Update statistics
        self.fps_label.config(text=f"{fps:.1f}")
        self.sign_label.config(text=hand_sign)
        self.gesture_label.config(text=gesture)
        self.conf_label.config(text=confidence)
        
        # Update history listbox
        self.history_listbox.delete(0, tk.END)
        for item in list(self.gesture_history)[-10:]:
            self.history_listbox.insert(tk.END, item)
        
        # Update collection counts
        self.count_collected_samples()
        self.kp_count_label.config(text=str(self.collected_samples["keypoint"]))
        self.gesture_count_label.config(text=str(self.collected_samples["gesture"]))
    
    def count_collected_samples(self):
        """Count collected training samples"""
        try:
            with open('model/keypoint_classifier/keypoint.csv', 'r') as f:
                self.collected_samples["keypoint"] = sum(1 for _ in f)
        except:
            self.collected_samples["keypoint"] = 0
        
        try:
            with open('model/point_history_classifier/point_history.csv', 'r') as f:
                self.collected_samples["gesture"] = sum(1 for _ in f)
        except:
            self.collected_samples["gesture"] = 0
    
    def logging_csv(self, number, mode, landmark_list, point_history_list):
        """Log data to CSV"""
        if mode == 0:
            pass
        if mode == 1 and (0 <= number <= 9):
            csv_path = 'model/keypoint_classifier/keypoint.csv'
            with open(csv_path, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *landmark_list])
        if mode == 2 and (0 <= number <= 9):
            csv_path = 'model/point_history_classifier/point_history.csv'
            with open(csv_path, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *point_history_list])
    
    def calc_landmark_list(self, image, landmarks):
        """Calculate landmark coordinates"""
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_point = []
        
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_point.append([landmark_x, landmark_y])
        
        return landmark_point
    
    def pre_process_landmark(self, landmark_list):
        """Preprocess landmarks"""
        temp_landmark_list = copy.deepcopy(landmark_list)
        
        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]
            
            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y
        
        temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))
        
        # Normalization
        max_value = max(list(map(abs, temp_landmark_list)))
        
        def normalize_(n):
            return n / max_value if max_value != 0 else 0
        
        temp_landmark_list = list(map(normalize_, temp_landmark_list))
        
        return temp_landmark_list
    
    def pre_process_point_history(self, image, point_history):
        """Preprocess point history"""
        image_width, image_height = image.shape[1], image.shape[0]
        temp_point_history = copy.deepcopy(point_history)
        
        base_x, base_y = 0, 0
        for index, point in enumerate(temp_point_history):
            if index == 0:
                base_x, base_y = point[0], point[1]
            
            temp_point_history[index][0] = (temp_point_history[index][0] - base_x) / image_width
            temp_point_history[index][1] = (temp_point_history[index][1] - base_y) / image_height
        
        temp_point_history = list(itertools.chain.from_iterable(temp_point_history))
        
        return temp_point_history
    
    def calc_bounding_rect(self, image, landmarks):
        """Calculate bounding rectangle"""
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_array = np.empty((0, 2), int)
        
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_point = [np.array((landmark_x, landmark_y))]
            landmark_array = np.append(landmark_array, landmark_point, axis=0)
        
        x, y, w, h = cv.boundingRect(landmark_array)
        return [x, y, x + w, y + h]
    
    def draw_bounding_rect(self, image, brect):
        """Draw bounding rectangle"""
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]), (0, 255, 0), 2)
        return image
    
    def draw_landmarks(self, image, landmark_point):
        """Draw hand landmarks"""
        if len(landmark_point) == 0:
            return image
        
        # Draw connections and keypoints
        connections = [
            (2, 3), (3, 4),  # Thumb
            (5, 6), (6, 7), (7, 8),  # Index
            (9, 10), (10, 11), (11, 12),  # Middle
            (13, 14), (14, 15), (15, 16),  # Ring
            (17, 18), (18, 19), (19, 20),  # Little
            (0, 1), (1, 2), (2, 5), (5, 9), (9, 13), (13, 17), (17, 0)  # Palm
        ]
        
        for start, end in connections:
            cv.line(image, tuple(landmark_point[start]), tuple(landmark_point[end]),
                   (0, 255, 0), 2)
        
        for idx, landmark in enumerate(landmark_point):
            size = 5 if idx not in [4, 8, 12, 16, 20] else 8
            cv.circle(image, tuple(landmark), size, (0, 255, 0), -1)
        
        return image
    
    def draw_point_history(self, image, point_history):
        """Draw finger movement history"""
        if len(point_history) > 0 and point_history[0] != [0, 0]:
            for index, point in enumerate(point_history):
                if point[0] != 0 and point[1] != 0:
                    alpha = (index + 1) / len(point_history)
                    cv.circle(image, tuple(point), int(5 * alpha), (255, 0, 0), -1)
        
        return image
    
    def draw_info_text(self, image, brect, handedness, hand_sign, gesture):
        """Draw information text"""
        cv.putText(image, f"{handedness.classification[0].label[0]}", 
                  (brect[0] + 5, brect[1] - 30),
                  cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv.putText(image, f"Sign: {hand_sign}", 
                  (brect[0] + 5, brect[1] - 10),
                  cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv.putText(image, f"Gesture: {gesture}", 
                  (brect[0] + 5, brect[1] + 15),
                  cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
        
        return image
    
    def draw_info(self, image, fps, mode, number):
        """Draw mode and FPS info"""
        mode_text = ["Normal", "Keypoint Collection", "Gesture Collection"][mode]
        cv.putText(image, f"FPS: {fps:.1f}", (10, 30),
                  cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv.putText(image, f"Mode: {mode_text}", (10, 70),
                  cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        if number != -1 and mode != 0:
            cv.putText(image, f"Collecting: {number}", (10, 110),
                      cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        return image


def main():
    root = tk.Tk()
    app = GestureRecognitionGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
