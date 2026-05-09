# 🎯 Professional GUI for Hand Gesture Recognition

## 🚀 Quick Start (2 Minutes)

```bash
# 1. Install dependencies
pip install -r requirements_gui.txt

# 2. Run the application
python run_gui.py
```

**That's it!** Your gesture recognition interface is now running. 🎉

---

## 📊 What You Get

```
┌──────────────────────────────────────┐
│  Hand Gesture Recognition System      │
├──────────────────────────────────────┤
│                                      │
│  📹 LIVE VIDEO                       │
│  ├─ Real-time hand detection         │
│  ├─ 21 landmark visualization        │
│  ├─ Gesture recognition overlay      │
│  └─ Multi-hand support (2 hands)     │
│                                      │
│  📊 STATISTICS DASHBOARD             │
│  ├─ FPS counter (20-30 FPS)          │
│  ├─ Hand sign recognition            │
│  ├─ Finger gesture detection         │
│  └─ Confidence scores                │
│                                      │
│  📝 GESTURE HISTORY                  │
│  ├─ Timestamped log                  │
│  ├─ Last 20 gestures                 │
│  └─ Easy reference timeline           │
│                                      │
│  🎓 DATA COLLECTION                  │
│  ├─ Collect training data            │
│  ├─ Auto-count samples               │
│  └─ Generate datasets (0-9 labels)   │
│                                      │
│  ℹ️  PROJECT INFO                    │
│  ├─ Quick specifications             │
│  ├─ Feature overview                 │
│  └─ Technical details                │
│                                      │
└──────────────────────────────────────┘
```

---

## 🎮 Interface Overview

### Main Window Layout

**Left Panel (60%):** Video display with hand landmarks  
**Right Panel (40%):** Controls and statistics

### Key Controls

| Control | Function |
|---------|----------|
| **▶ Start Camera** | Begin real-time detection |
| **⏹ Stop Camera** | Stop detection and close camera |
| **Mode Selection** | Choose Normal, Gesture Collection, or Finger Gesture Collection |

### Information Displays

| Panel | Shows |
|-------|-------|
| **Real-time Statistics** | FPS, Hand Sign, Gesture, Confidence |
| **Gesture History** | Last 20 recognized gestures with timestamps |
| **Data Collection** | Count of collected samples for training |
| **Project Info** | Quick reference to project capabilities |

---

## 📈 Features

### ✨ Real-time Inference
- Detects hand poses instantly
- Classifies 5 hand signs: Open, Close, Pointer, OK, Peace
- Recognizes 4 finger gestures: Stop, Clockwise, Counter-Clockwise, Move
- Supports 2 hands simultaneously
- Smooth 20-30 FPS performance

### 🎬 Live Visualization
- Hand skeleton with all 21 landmarks
- Gesture labels overlaid on video
- Bounding boxes around detected hands
- Pointing finger trail showing motion history
- Hand identification (Left/Right)

### 📊 Statistics & Monitoring
- Real-time FPS display
- Recognition confidence percentage
- Gesture history with timestamps
- Collection progress tracker
- Performance metrics

### 🎓 Data Collection Mode
- Easy toggle between modes
- Collect hand sign training data
- Collect finger gesture training data
- Automatic CSV logging
- Sample counter

### 🔍 Debugging Tools
- Visual landmarks on live feed
- Confidence scores displayed
- Mode indicator
- Sample collection counter
- Performance metrics

---

## 🎯 Use Cases

### 1. **Demonstration & Presentation**
```
Show clients/stakeholders:
✓ Real-time gesture recognition
✓ Hand tracking accuracy
✓ Live performance metrics
✓ Professional interface
```

### 2. **Development & Testing**
```
Test and verify:
✓ Model inference quality
✓ Performance metrics
✓ Detection accuracy
✓ Edge cases
```

### 3. **Data Collection & Training**
```
Build custom models:
✓ Collect gesture samples
✓ Label data interactively
✓ Generate datasets
✓ Train custom models (via notebooks)
```

### 4. **Interactive Application**
```
Deploy as:
✓ Standalone application
✓ Demo kiosk software
✓ Interactive installation
✓ Educational tool
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **GUI_QUICK_START.md** | Get started in 30 seconds |
| **GUI_README.md** | Detailed feature documentation |
| **GUI_FEATURES.md** | Complete technical specifications |
| **INSTALLATION_GUIDE.md** | Setup and troubleshooting |
| **gui_config.py** | Configuration and customization |

---

## 🔧 System Requirements

### Minimum
- Python 3.8+
- 4GB RAM
- USB Webcam
- Windows/macOS/Linux

### Recommended
- Python 3.10+
- 8GB+ RAM
- 1080p Webcam
- Intel i7 or better CPU
- SSD storage

---

## 📦 Installation

### 1. Prerequisites
```bash
# Ensure Python 3.8+ is installed
python --version
```

### 2. Install Dependencies
```bash
# From project directory
pip install -r requirements_gui.txt
```

### 3. Verify Installation
```bash
# Run verification script
python run_gui.py  # This checks all dependencies
```

### 4. Launch GUI
```bash
# Start the application
python gui_app.py
```

**For detailed installation help**, see [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

---

## 🎬 How to Use

### Normal Mode (Inference)

```
1. Click "▶ Start Camera"
2. Position hand in front of camera
3. System recognizes gesture in real-time
4. Results displayed in statistics panel
5. Gesture added to history timeline
6. Click "⏹ Stop Camera" to finish
```

### Data Collection Mode

```
1. Select "Collect Gestures (0-9)" or "Collect Finger Gestures (0-9)"
2. Click "▶ Start Camera"
3. Perform gesture
4. Press number key (0-9) to label and save
5. Repeat for 20-50 samples per gesture
6. Use data to train models (see notebooks)
```

---

## 📊 Statistics Explained

### FPS (Frames Per Second)
- **Target**: 25-30 FPS
- **Good**: 20+ FPS (smooth real-time)
- **Poor**: <10 FPS (lag visible)
- **Factors**: Hardware, lighting, complexity

### Hand Sign
- The recognized static gesture
- One of: Open, Close, Pointer, OK, Peace
- Updated every frame

### Gesture
- The recognized dynamic motion
- One of: Stop, Clockwise, Counter-Clockwise, Move
- Updated when finger is pointing

### Confidence
- Prediction certainty (0-1 or 0-100%)
- Higher is better (>0.7 is good)
- Lower values may indicate uncertain prediction

---

## 🎓 Training Custom Models

After collecting data in the GUI:

1. **Export Data** (GUI automatically saves to CSV)
   - Hand signs: `model/keypoint_classifier/keypoint.csv`
   - Gestures: `model/point_history_classifier/point_history.csv`

2. **Retrain Model** (Use provided notebooks)
   ```bash
   # Use Jupyter notebooks:
   # - keypoint_classification.ipynb (for hand signs)
   # - point_history_classification.ipynb (for gestures)
   ```

3. **Test New Model** (In GUI)
   ```
   - New model auto-loads at startup
   - Test with GUI in Normal mode
   - Verify accuracy
   ```

---

## ⚙️ Customization

### Modify Appearance
- Edit colors in `gui_config.py`
- Adjust window size
- Change font sizes

### Adjust Performance
- Modify detection confidence thresholds
- Change video resolution
- Tune gesture recognition parameters

### Extend Functionality
- Add gesture logging
- Export statistics
- Record videos
- Add custom visualizations

See [gui_config.py](gui_config.py) for all options.

---

## 🐛 Troubleshooting

### Camera Won't Start
```
Problem: "Cannot open camera" error

Solutions:
□ Close other camera apps (Zoom, Teams)
□ Check camera permissions
□ Try different camera device (modify device=1)
□ Restart application
```

### Low FPS
```
Problem: Slow performance (<10 FPS)

Solutions:
□ Close background applications
□ Reduce video resolution
□ Lower detection confidence
□ Use faster hardware
```

### Poor Hand Detection
```
Problem: Hands not recognized

Solutions:
□ Improve lighting
□ Position hand fully in frame
□ Get closer to camera (0.5-1m)
□ Clean camera lens
□ Use uniform background
```

### Data Not Saving
```
Problem: Collection data not appearing

Solutions:
□ Ensure mode is set to "Collect"
□ Press number key 0-9 after gesture
□ Check file permissions
□ Verify CSV files exist
```

**For more help**, see [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

---

## 🎯 Performance Tips

### For Better Recognition
✓ Good lighting (natural light preferred)  
✓ Clean camera lens  
✓ 0.5-1 meter distance from camera  
✓ Show complete hand in frame  
✓ Consistent background  

### For Better Performance
✓ Close unnecessary applications  
✓ Use wired connection (not WiFi) if on network  
✓ Reduce video resolution if needed  
✓ Use modern hardware (i7+ recommended)  

### For Best Results
✓ Train custom model with your data  
✓ Collect diverse gesture samples  
✓ Test in actual deployment environment  
✓ Monitor confidence scores  

---

## 🔗 Integration

### As Standalone App
```python
python gui_app.py
```

### As Python Module
```python
from gui_app import GestureRecognitionGUI
import tkinter as tk

root = tk.Tk()
app = GestureRecognitionGUI(root)
root.mainloop()
```

### As Executable (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed gui_app.py
# Creates: dist/gui_app.exe
```

---

## 📚 Additional Resources

| Resource | Details |
|----------|---------|
| **Original Project** | See README.md for original CLI app |
| **MediaPipe Docs** | https://mediapipe.dev |
| **TensorFlow Lite** | https://www.tensorflow.org/lite |
| **OpenCV Docs** | https://docs.opencv.org |

---

## 🤝 Contributing

Found a bug or want to improve the GUI?

1. Test the feature thoroughly
2. Document the issue
3. Propose a solution
4. Submit changes

---

## 📝 License

Same as original project. See [LICENSE](LICENSE)

---

## ✨ What's New

### Compared to Original CLI App

| Feature | Original | GUI |
|---------|----------|-----|
| User Interface | Terminal/CLI | Professional GUI |
| Visual Feedback | Text output | Live video |
| Statistics | Limited | Comprehensive dashboard |
| Gesture History | None | Timestamped timeline |
| Data Collection | Command-line | Easy buttons and counters |
| Performance Metrics | Basic FPS | Detailed statistics |
| User Experience | Technical | User-friendly |

---

## 🎬 Demo Workflow

```
START HERE
    ↓
1. Run: python run_gui.py
    ↓
2. Click "▶ Start Camera"
    ↓
3. Show hand gestures
    ↓
4. Watch real-time recognition
    ↓
5. Check gesture history
    ↓
6. Collect data (optional)
    ↓
READY FOR PRODUCTION
```

---

## 💡 Pro Tips

- **Keyboard Shortcuts**: Use number keys (0-9) in collection mode
- **Multiple Hands**: Show both hands for simultaneous tracking
- **Performance**: Monitor FPS in statistics panel
- **Data Quality**: Collect diverse samples for better models
- **Timestamps**: History shows exact recognition times
- **Export**: Data automatically saved to CSV for analysis

---

## 🎓 Learning Resources

After mastering the GUI, explore:
- Custom gesture recognition
- Multi-gesture sequences
- Hand pose estimation
- Gesture-controlled applications
- Real-time video processing
- TensorFlow Lite optimization

---

## 📞 Support

If you need help:

1. **Quick Start**: See [GUI_QUICK_START.md](GUI_QUICK_START.md)
2. **Installation Issues**: See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
3. **Feature Details**: See [GUI_FEATURES.md](GUI_FEATURES.md)
4. **Configuration**: See [gui_config.py](gui_config.py)
5. **General Help**: See original [README.md](README.md)

---

## 🚀 Ready to Get Started?

```bash
# 1. Install
pip install -r requirements_gui.txt

# 2. Run
python run_gui.py

# 3. Enjoy!
# 🎉 Your gesture recognition interface is ready
```

---

**GUI Version**: 1.0  
**Last Updated**: April 2026  
**Status**: Production Ready ✅

**Built with ❤️ using Python, MediaPipe, and TensorFlow Lite**
