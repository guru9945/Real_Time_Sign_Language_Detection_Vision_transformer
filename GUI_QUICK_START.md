# GUI Quick Start Guide

## 🚀 Fast Start (30 seconds)

```bash
# 1. Install dependencies
pip install mediapipe opencv-python tensorflow numpy pillow

# 2. Run the GUI
python run_gui.py

# Or directly
python gui_app.py
```

---

## 📊 Interface Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  Hand Gesture Recognition System                                │
├──────────────────────────────┬──────────────────────────────────┤
│                              │ ▶ START CAMERA   ⏹ STOP CAMERA   │
│                              ├──────────────────────────────────┤
│                              │ Mode: ○ Normal                   │
│                              │       ○ Collect Gestures (0-9)   │
│                              │       ○ Collect Finger Gest. (0-9)│
│                              ├──────────────────────────────────┤
│                              │ FPS: 28.5                        │
│   LIVE VIDEO FEED            │ Hand Sign: Open                  │
│   (640x480)                  │ Gesture: --                      │
│                              │ Confidence: 0.95                 │
│                              ├──────────────────────────────────┤
│                              │ Gesture History                  │
│                              │ [14:32:01] Open                  │
│                              │ [14:32:02] Close - Stop          │
│                              │ [14:32:03] Pointer - Move        │
│                              │ [14:32:04] OK                    │
│                              ├──────────────────────────────────┤
│                              │ Data Collection                  │
│                              │ Hand Gestures: 245               │
│                              │ Finger Gestures: 189             │
│                              ├──────────────────────────────────┤
│                              │ Project Info                     │
│                              │ ✓ Real-time detection            │
│                              │ ✓ 21 hand landmarks              │
└──────────────────────────────┴──────────────────────────────────┘
```

---

## 🎮 Main Operations

### **Start Recognition**
1. Click **"▶ Start Camera"** button
2. Position hand in front of camera
3. Recognized gesture appears in top-right
4. Statistics update in real-time

### **Collect Training Data**

#### For Hand Signs (0-9 poses):
```
1. Select "Collect Gestures (0-9)"
2. Start camera
3. Show pose (e.g., Open hand)
4. Press key 0-9 to label
5. Repeat for 20-30 samples per pose
6. Use keypoint_classification.ipynb to retrain
```

#### For Finger Gestures (0-9 motions):
```
1. Select "Collect Finger Gestures (0-9)"
2. Start camera
3. Make pointing gesture and move it
4. Press key 0-9 to label
5. Collect 20-30 samples per gesture
6. Use point_history_classification.ipynb to retrain
```

---

## 📈 Live Statistics Explained

| Metric | Meaning | Normal Range |
|--------|---------|--------------|
| **FPS** | Frames per second | 20-30 |
| **Hand Sign** | Static gesture recognized | Open, Close, Pointer, OK, Peace |
| **Gesture** | Dynamic motion recognized | Stop, Clockwise, CCW, Move |
| **Confidence** | Prediction confidence | >0.7 (good), <0.5 (uncertain) |

---

## 🎯 Tips for Best Results

### **For Inference (Normal Mode)**
- ✅ Good lighting on hands
- ✅ 0.5-1 meter distance from camera
- ✅ Show clear hand poses
- ✅ Avoid shadows and reflections

### **For Data Collection**
- ✅ Collect 20-50 samples per class
- ✅ Vary hand size and position
- ✅ Vary hand angle
- ✅ Include edge cases (fast motion, different lighting)
- ✅ Maintain consistent background for collection

---

## 🔄 Workflow: Train Custom Model

```
┌─────────────────────────┐
│ 1. Collect Data         │
│    gui_app.py           │
└────────┬────────────────┘
         │
         ↓
┌─────────────────────────┐
│ 2. Retrain Model        │
│ keypoint_classification │
│      .ipynb             │
└────────┬────────────────┘
         │
         ↓
┌─────────────────────────┐
│ 3. Test in GUI          │
│    gui_app.py           │
│ (uses new .tflite)      │
└─────────────────────────┘
```

---

## ⚙️ Keyboard Controls

When camera is active, you can:

| Key | Action |
|-----|--------|
| `0-9` | Label and collect data (collection mode only) |
| `ESC` or close window | Stop camera |

---

## 🐛 Troubleshooting

### Camera won't start
```
✗ Error: "Cannot open camera"
✓ Solution: 
  - Check camera is connected
  - Close other camera apps (Zoom, Teams, etc.)
  - Try: python gui_app.py  # Run directly
```

### Low FPS (< 10)
```
✗ Problem: Detection is too slow
✓ Solutions:
  - Close background applications
  - Reduce resolution in code
  - Use smaller model
  - Upgrade hardware
```

### No hand detection
```
✗ Problem: Hands not recognized
✓ Solutions:
  - Improve lighting
  - Show full hand in frame
  - Get closer to camera (0.5-1m)
  - Ensure clean background
```

### Data not saving
```
✗ Problem: CSV files not updating
✓ Solutions:
  - Ensure mode is set to "Collect" (not Normal)
  - Press number key 0-9 after showing gesture
  - Check file permissions
  - Verify CSV files exist
```

---

## 📂 Data Location

After collecting, find data in:

```
model/
├── keypoint_classifier/
│   └── keypoint.csv          ← Hand sign data (class, x1, y1, x2, y2, ...)
└── point_history_classifier/
    └── point_history.csv     ← Gesture data (class, x_hist, y_hist, ...)
```

Each row format:
- **Keypoint CSV**: `[gesture_id, feature1, feature2, ..., feature42]`
- **History CSV**: `[gesture_id, feature1, feature2, ..., feature32]`

---

## 🎓 Learning Resources

After mastering the GUI, explore:
1. **Modify models**: Edit `keypoint_classification.ipynb`
2. **Add features**: Extend `gui_app.py`
3. **Export data**: Save gesture videos and statistics
4. **Deploy**: Convert to .exe or web app

---

## ✨ What's New in GUI Version

| Feature | Original CLI | GUI |
|---------|-------------|-----|
| Visual Feedback | Terminal text | Live video window |
| Real-time Stats | Limited | Full dashboard |
| Gesture History | None | Timeline with timestamps |
| Data Counter | Manual | Auto-count samples |
| Mode Switching | Keyboard only | Radio buttons |
| FPS Display | Simple | Detailed |
| User Experience | Minimal | Professional |

---

**Need Help?** Check `GUI_README.md` for detailed documentation
