# GUI Features & Architecture Documentation

## 📋 Complete Feature List

### ✅ Core Features

#### 1. **Live Real-time Video Feed**
- Live webcam capture (960x540 resolution, resizable)
- Real-time hand detection using MediaPipe
- Support for up to 2 hands simultaneously
- Display in 640x480 format (optimized for viewing)
- Smooth frame updates at 20-30 FPS

#### 2. **Hand Visualization**
- **Hand Skeleton**: Visual lines connecting hand landmarks
- **Key Points**: 21 landmark points marked with circles
  - Larger circles for joint tips (thumb, index, etc.)
  - Smaller circles for joint bases
- **Bounding Boxes**: Green rectangles around detected hands
- **Hand Labels**: Left/Right hand identification

#### 3. **Gesture Recognition Display**
- **Hand Signs**: Open, Close, Pointer, OK, Peace
- **Finger Gestures**: Stop, Clockwise, Counter-Clockwise, Move
- **Pointing Trail**: Blue dots showing finger movement history
- **Real-time Labels**: Gesture names displayed on video

#### 4. **Real-time Statistics Dashboard**

| Metric | Display | Update Rate |
|--------|---------|------------|
| FPS | Frames per second (target: 25-30) | Per frame |
| Hand Sign | Current gesture (name) | Per detection |
| Finger Gesture | Current motion (name) | Per detection cycle |
| Confidence | Prediction confidence % | Per detection |

#### 5. **Gesture History Timeline**
- Timestamped log of all recognized gestures
- Shows both hand signs and finger gestures
- Last 20 entries visible
- Auto-scrolls to latest
- Format: `[HH:MM:SS] Gesture_Name`

#### 6. **Data Collection Mode**
- **Three Operating Modes**:
  1. **Normal**: Pure inference/recognition
  2. **Hand Gesture Collection**: Collect poses (0-9 labels)
  3. **Finger Gesture Collection**: Collect motions (0-9 labels)

- **Data Flow**:
  - Press mode button → Camera activates
  - Perform gesture
  - Press number key (0-9) → Data labeled and saved to CSV

- **Data Saved**:
  - Keypoint data: 42 normalized features (21 landmarks × 2 coordinates)
  - Gesture data: 32 features (16 frames × 2 coordinates)

#### 7. **Collection Statistics**
- Live counter for hand gesture samples collected
- Live counter for finger gesture samples collected
- Updates every frame when collecting
- Used for training progress tracking

#### 8. **Project Information Panel**
- Quick reference card
- Shows project capabilities
- Displays key features and specifications

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   GUI Application (tkinter)                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐        ┌──────────────────────────┐   │
│  │  Camera Thread   │        │  Main UI Thread          │   │
│  │                  │        │                          │   │
│  │ • Capture frames │        │ • Update labels          │   │
│  │ • Process video  │◄──────►│ • Draw statistics        │   │
│  │ • Run inference  │        │ • Handle user input      │   │
│  │ • Update history │        │ • Manage modes           │   │
│  └──────────────────┘        └──────────────────────────┘   │
│         │                             │                       │
│         ├────────────┬────────────────┤                       │
│         │            │                │                       │
│         ▼            ▼                ▼                       │
│    ┌─────────┐ ┌──────────┐ ┌──────────────┐               │
│    │ MediaPipe  │ TFLite    │ CSV Logger    │               │
│    │ Hand     │ Models    │ (Data collect)│               │
│    │ Detection│ (Keypoint)│              │               │
│    │          │ (History) │              │               │
│    └─────────┘ └──────────┘ └──────────────┘               │
│         │            │                │                       │
│         └────────────┴────────────────┘                       │
│                      │                                         │
│              ┌────────▼────────┐                               │
│              │ Frame Processing │                               │
│              │  • Landmark calc │                               │
│              │  • Normalization │                               │
│              │  • Preprocessing │                               │
│              └──────────────────┘                               │
│                                                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

### Inference Mode
```
Video Frame
    ↓
MediaPipe Hands Detection (21 landmarks)
    ↓
Preprocess: Normalize & Relativize
    ↓
KeyPoint Classifier (TFLite)
    ↓
Hand Sign Recognized (Open/Close/Pointer/OK/Peace)
    ├─→ Display on UI ✓
    └─→ Add to History ✓
    
    IF Hand Sign == "Pointer":
        ├─→ Track Finger Tip (Point 8)
        └─→ Add to Point History
    
    IF Point History Complete (16 frames):
        ├─→ Gesture Classifier (TFLite)
        └─→ Gesture Recognized (Stop/CW/CCW/Move)
            ├─→ Display on UI ✓
            └─→ Add to History ✓
```

### Data Collection Mode
```
Video Frame
    ↓
[Same as Inference...]
    ↓
Hand Sign Recognized
    ↓
USER PRESSES KEY (0-9)
    ↓
Log to CSV: [class_id, feature_1, feature_2, ..., feature_N]
    ↓
File: model/keypoint_classifier/keypoint.csv
    ├─→ Update sample counter ✓
    └─→ Ready for retraining ✓
```

---

## 📊 UI Layout Breakdown

```
┌─────────────────────────────────────────────────────────────────┐
│ WINDOW TITLE: Hand Gesture Recognition System (1400 x 900)      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  LEFT PANEL (60%)              RIGHT PANEL (40%, width: 350px)  │
│  ┌───────────────────┐        ┌──────────────────────────────┐ │
│  │  Live Feed        │        │ Control Panel                │ │
│  │  640 x 480        │        │ ┌──────────────────────────┐ │ │
│  │                   │        │ │ ▶START  ⏹STOP            │ │ │
│  │ [Video Stream]    │        │ │ Mode: ○ Normal           │ │ │
│  │                   │        │ │       ○ Collect Gest.    │ │ │
│  │ • Landmarks       │        │ │       ○ Collect Finger   │ │ │
│  │ • Skeleton        │        │ └──────────────────────────┘ │ │
│  │ • Trail           │        ├──────────────────────────────┤ │
│  │ • Labels          │        │ Real-time Statistics         │ │
│  │                   │        │ FPS: 28.5                    │ │
│  │                   │        │ Hand Sign: Open              │ │
│  │                   │        │ Gesture: --                  │ │
│  │                   │        │ Confidence: 0.95             │ │
│  └───────────────────┘        ├──────────────────────────────┤ │
│                               │ Gesture History (20 items)   │ │
│                               │ ┌──────────────────────────┐ │ │
│                               │ │ [14:32:01] Open          │ │ │
│                               │ │ [14:32:02] Close - Stop  │ │ │
│                               │ │ [14:32:03] Pointer-Move  │ │ │
│                               │ │ ...                      │ │ │
│                               │ └──────────────────────────┘ │ │
│                               ├──────────────────────────────┤ │
│                               │ Data Collection              │ │
│                               │ Hand Gestures: 245           │ │
│                               │ Finger Gestures: 189         │ │
│                               ├──────────────────────────────┤ │
│                               │ Project Info                 │ │
│                               │ ✓ Real-time detection        │ │
│                               │ ✓ 21 hand landmarks          │ │
│                               │ ✓ 5 Hand signs               │ │
│                               │ ✓ 4 Finger gestures          │ │
│                               └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔌 Component Integration

### External Dependencies
```
gui_app.py
├── tkinter          (GUI framework)
├── threading        (Async camera processing)
├── cv2              (OpenCV - image processing)
├── mediapipe        (Hand detection)
├── tensorflow       (TFLite inference)
├── numpy            (Array operations)
├── PIL              (Image conversion)
├── csv              (Data logging)
└── datetime         (Timestamps)
```

### Project Integration
```
gui_app.py
├── model/keypoint_classifier/keypoint_classifier.py
├── model/point_history_classifier/point_history_classifier.py
├── utils/cvfpscalc.py
├── model/keypoint_classifier/keypoint_classifier.tflite
├── model/point_history_classifier/point_history_classifier.tflite
├── model/keypoint_classifier/keypoint_classifier_label.csv
├── model/point_history_classifier/point_history_classifier_label.csv
└── Generated:
    ├── model/keypoint_classifier/keypoint.csv
    └── model/point_history_classifier/point_history.csv
```

---

## ⚡ Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| **Frame Rate** | 25-30 FPS | Depends on hardware |
| **Latency** | ~30-50ms | Detection to display |
| **Memory** | ~200-300 MB | GUI + Models |
| **CPU Usage** | 20-40% | Single core, i5-class CPU |
| **GPU Support** | Optional | Can accelerate with CUDA |

---

## 🎯 Use Cases

### 1. **Real-time Inference**
- Interactive gesture recognition
- Live feedback system
- Demo and presentation

### 2. **Data Collection**
- Build custom datasets
- Create domain-specific models
- Generate training data

### 3. **Performance Tuning**
- FPS monitoring
- Confidence analysis
- Detection quality assessment

### 4. **Application Development**
- Visual debugging
- Model validation
- Integration testing

---

## 🔧 Extensibility Points

Users can customize:
1. **Models**: Replace .tflite files with custom trained models
2. **Labels**: Edit CSV label files to add new gestures
3. **UI**: Modify tkinter layout and colors
4. **Inference**: Add custom preprocessing or postprocessing
5. **Data Export**: Export statistics and videos
6. **Visualization**: Add heatmaps or confidence graphs

---

## 📈 Advanced Features (Future)

Potential enhancements:
- [ ] Video recording with overlay
- [ ] Statistics export (CSV, JSON)
- [ ] Gesture sequence recognition
- [ ] Multi-gesture combinations
- [ ] Confidence heatmaps
- [ ] Performance profiling
- [ ] Model optimization tools
- [ ] REST API for remote inference

---

## 🎓 Learning Outcomes

Users will understand:
- ✅ Real-time computer vision pipeline
- ✅ MediaPipe hand detection capabilities
- ✅ TensorFlow Lite inference optimization
- ✅ GUI design with tkinter
- ✅ Threading and async processing
- ✅ Data collection and preprocessing
- ✅ Model evaluation metrics
- ✅ Production-ready code structure

---

**Document Version**: 1.0  
**Last Updated**: April 2026  
**Compatibility**: Python 3.8+
