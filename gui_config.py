"""
GUI Configuration File
Customize these settings to adjust the GUI behavior
"""

# ============================================================================
# CAMERA SETTINGS
# ============================================================================

# Camera device index (0 = default webcam, 1, 2, ... for multiple cameras)
CAMERA_DEVICE = 0

# Video resolution
VIDEO_WIDTH = 960
VIDEO_HEIGHT = 540

# Display resolution in GUI
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# ============================================================================
# MEDIAPIPE SETTINGS
# ============================================================================

# Hand detection confidence threshold (0.0 - 1.0)
# Higher = more conservative detection, fewer false positives
MIN_DETECTION_CONFIDENCE = 0.7

# Hand tracking confidence threshold (0.0 - 1.0)
MIN_TRACKING_CONFIDENCE = 0.5

# Maximum number of hands to detect (1 or 2)
MAX_NUM_HANDS = 2

# Use static image mode (slower but more accurate)
USE_STATIC_IMAGE_MODE = False

# ============================================================================
# MODEL SETTINGS
# ============================================================================

# Keypoint classifier confidence threshold
# Predictions below this are ignored
KEYPOINT_CONFIDENCE_THRESHOLD = 0.5

# Point history (gesture) classifier confidence threshold
GESTURE_CONFIDENCE_THRESHOLD = 0.5

# Number of frames to track for gesture history
HISTORY_LENGTH = 16

# Number of frames to keep in gesture history for display
DISPLAY_HISTORY_LENGTH = 20

# ============================================================================
# GUI SETTINGS
# ============================================================================

# Window title
WINDOW_TITLE = "Hand Gesture Recognition System"

# Window size
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# Theme color scheme
BG_COLOR = "#f0f0f0"
ACCENT_COLOR = "#0078d4"

# Font settings
FONT_FAMILY = "Arial"
FONT_SIZE_TITLE = 14
FONT_SIZE_NORMAL = 10
FONT_SIZE_SMALL = 8

# FPS buffer for smoothing
FPS_BUFFER_LENGTH = 10

# ============================================================================
# DATA COLLECTION SETTINGS
# ============================================================================

# Keypoint CSV file path
KEYPOINT_CSV_PATH = 'model/keypoint_classifier/keypoint.csv'

# Point history CSV file path
GESTURE_CSV_PATH = 'model/point_history_classifier/point_history.csv'

# Number of samples to show in statistics
COLLECTION_STATS_UPDATE_INTERVAL = 5  # Update every N frames

# ============================================================================
# VISUALIZATION SETTINGS
# ============================================================================

# Draw bounding boxes
DRAW_BOUNDING_BOXES = True

# Draw hand landmarks
DRAW_LANDMARKS = True

# Draw point history trail
DRAW_POINT_HISTORY = True

# Landmark colors (BGR format)
LANDMARK_COLOR = (0, 255, 0)  # Green
KEYPOINT_COLOR = (0, 255, 0)  # Green
BOUNDING_BOX_COLOR = (0, 255, 0)  # Green
POINT_HISTORY_COLOR = (255, 0, 0)  # Blue
TEXT_COLOR = (255, 255, 255)  # White

# Line thickness
LINE_THICKNESS = 2
LANDMARK_RADIUS = 5
KEYPOINT_RADIUS = 8

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================

# Number of threads for TFLite inference
NUM_THREADS = 1

# Update UI every N frames (1 = every frame)
UI_UPDATE_INTERVAL = 1

# Enable GPU acceleration (if available)
USE_GPU = False

# ============================================================================
# LOGGING SETTINGS
# ============================================================================

# Enable console logging
ENABLE_LOGGING = True

# Log level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = "INFO"

# Save statistics to file
SAVE_STATISTICS = True

# Statistics file path
STATS_FILE_PATH = "gesture_stats.csv"

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

# Gesture voting window (use most common gesture in last N frames)
GESTURE_VOTING_WINDOW = 10

# Minimum hand area to detect (pixels)
MIN_HAND_AREA = 100

# Enable hand smoothing (temporal filtering)
ENABLE_SMOOTHING = True

# Smoothing factor (0.0 - 1.0, higher = more smoothing)
SMOOTHING_FACTOR = 0.7

# ============================================================================
# KEY MAPPINGS (for data collection mode)
# ============================================================================

# Number keys (0-9) to gesture IDs
# When in collection mode, pressing these keys labels and saves the gesture
KEY_MAPPINGS = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
}

# ============================================================================
# BUTTON MAPPINGS
# ============================================================================

# Keyboard shortcuts for mode switching (when camera is running)
MODE_SHORTCUTS = {
    'n': 0,  # Normal mode
    'k': 1,  # Keypoint collection
    'h': 2,  # Gesture collection
}

# ============================================================================
# END OF CONFIGURATION
# ============================================================================

"""
USAGE:
------
To use custom configuration:

    from config import *
    
    # Now use settings like:
    cap.set(cv.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)

EXAMPLE CONFIGURATIONS:
-----------------------

Fast Detection (Mobile-oriented):
    MIN_DETECTION_CONFIDENCE = 0.5
    MIN_TRACKING_CONFIDENCE = 0.3
    HISTORY_LENGTH = 8
    NUM_THREADS = 1

High Accuracy (Desktop-oriented):
    MIN_DETECTION_CONFIDENCE = 0.9
    MIN_TRACKING_CONFIDENCE = 0.7
    HISTORY_LENGTH = 16
    NUM_THREADS = 4

Edge Device (Raspberry Pi, etc):
    VIDEO_WIDTH = 640
    VIDEO_HEIGHT = 480
    DISPLAY_WIDTH = 320
    DISPLAY_HEIGHT = 240
    MIN_DETECTION_CONFIDENCE = 0.6
    NUM_THREADS = 1
"""
