# GUI Application Setup Guide

## Overview
This is a professional Tkinter-based desktop GUI for the Hand Gesture Recognition project. It provides real-time gesture recognition with visualization, statistics, and data collection capabilities.

## Features Included

### 1. **Live Video Feed**
- Real-time camera feed with hand detection
- Bounding boxes around detected hands
- Hand skeleton visualization with landmarks
- Support for up to 2 hands simultaneously

### 2. **Real-time Statistics Panel**
- **FPS**: Displays frames per second
- **Hand Sign**: Current recognized gesture (Open, Close, Pointer, OK, Peace)
- **Finger Gesture**: Dynamic gesture recognition (Stop, Clockwise, Counter-Clockwise, Move)
- **Confidence**: Confidence level of predictions

### 3. **Gesture History Timeline**
- Displays last 20 recognized gestures with timestamps
- Shows both hand signs and finger gestures
- Automatically scrolls to show latest gestures

### 4. **Data Collection Interface**
- Three operation modes:
  - **Normal**: Pure inference mode
  - **Collect Hand Gestures**: Collect training data for hand signs (0-9)
  - **Collect Finger Gestures**: Collect training data for finger gestures (0-9)
- Real-time counter for collected samples
- Data automatically saved to CSV files

### 5. **Project Information Panel**
- Quick reference guide
- Key statistics about the project

## Installation

### Requirements
```bash
pip install mediapipe opencv-python tensorflow numpy pillow
```

### Running the GUI

```bash
python gui_app.py
```

## How to Use

### Normal Mode (Inference)
1. Click **"▶ Start Camera"** button
2. Show hand gestures to the camera
3. Recognized gestures appear in the statistics panel and history

### Data Collection Mode

#### Hand Gesture Collection
1. Select **"Collect Gestures (0-9)"** radio button
2. Click **"▶ Start Camera"**
3. Perform a gesture (e.g., Open hand)
4. Press a number key (0-9) to assign and collect it
5. Repeat for different poses
6. Data saved to: `model/keypoint_classifier/keypoint.csv`

#### Finger Gesture Collection
1. Select **"Collect Finger Gestures (0-9)"** radio button
2. Click **"▶ Start Camera"**
3. Make a pointing gesture, then move in a pattern
4. Press a number key (0-9) to assign and collect it
5. Data saved to: `model/point_history_classifier/point_history.csv`

## Keyboard Controls

When camera is running:
- **Number keys (0-9)**: Label and collect data (in collection modes)
- **Close window or click Stop**: Stop camera

## Architecture

The GUI integrates with your existing project:

```
gui_app.py
    ├── Uses existing models
    │   ├── model/keypoint_classifier/keypoint_classifier.tflite
    │   └── model/point_history_classifier/point_history_classifier.tflite
    │
    └── Generates/Updates
        ├── model/keypoint_classifier/keypoint.csv
        └── model/point_history_classifier/point_history.csv
```

## File Structure After GUI Creation

```
hand-gesture-recognition-mediapipe-main/
├── app.py                           # Original CLI app
├── gui_app.py                       # NEW: GUI application
├── GUI_README.md                    # NEW: This file
├── model/
│   ├── keypoint_classifier/
│   │   ├── keypoint_classifier.tflite
│   │   ├── keypoint_classifier_label.csv
│   │   └── keypoint.csv            # Updated when collecting data
│   └── point_history_classifier/
│       ├── point_history_classifier.tflite
│       ├── point_history_classifier_label.csv
│       └── point_history.csv       # Updated when collecting data
└── utils/
    └── cvfpscalc.py
```

## Performance Tips

1. **Optimal Lighting**: Ensure good lighting for better hand detection
2. **Camera Distance**: Keep hand 0.5-1 meter from camera
3. **Background**: Clutter-free background improves detection
4. **FPS**: Should maintain 20-30 FPS on standard hardware

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Camera not detected | Check camera device in settings, try `--device 1` |
| Low FPS | Close other applications, reduce resolution |
| Poor detection | Improve lighting, ensure hand is visible in frame |
| CSV data not saving | Ensure CSV files exist in model directories |

## Next Steps: Retraining

After collecting training data, retrain models using:
- `keypoint_classification.ipynb` for hand signs
- `point_history_classification.ipynb` for finger gestures

## Extending the GUI

You can customize:
- Resolution: Modify video dimensions
- Detection confidence thresholds
- Add more gesture classes
- Export statistics to CSV
- Add video recording capability

---

**Developed for Hand Gesture Recognition Project**
Showcasing real-time computer vision with MediaPipe and TensorFlow Lite
