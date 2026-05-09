# Requirements for GUI Application

## Minimum Requirements

### Operating System
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+)

### Hardware
- Processor: Intel i5 or equivalent (or better)
- RAM: 4GB minimum (8GB recommended)
- Webcam: Standard USB webcam or built-in camera
- GPU: Optional (for faster inference)

### Python
- Python 3.8 or higher
- pip package manager

---

## Python Dependencies

### Core Libraries
```
mediapipe>=0.8.1          # Hand detection
opencv-python>=3.4.2      # Computer vision
tensorflow>=2.3.0         # TFLite runtime
numpy>=1.19.0             # Numerical computing
pillow>=8.0.0             # Image processing
```

### GUI Framework
```
tkinter                   # Built-in with Python (usually)
```

### Optional (for development)
```
jupyter>=1.0.0            # For notebooks
scikit-learn>=0.23.2      # For model metrics
matplotlib>=3.3.2         # For plotting
```

---

## Installation Steps

### 1. Install Python
Download from [python.org](https://www.python.org) (3.8 or higher)

### 2. Clone/Download Project
```bash
git clone <repository-url>
cd hand-gesture-recognition-mediapipe-main
```

### 3. Create Virtual Environment (Recommended)

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Required Packages

#### Quick Install (All dependencies):
```bash
pip install -r requirements_gui.txt
```

#### Manual Install:
```bash
pip install mediapipe
pip install opencv-python
pip install tensorflow
pip install numpy
pip install pillow
```

### 5. Verify Installation
```bash
python -c "import cv2, mediapipe, tensorflow; print('✓ All packages installed')"
```

### 6. Run GUI Application
```bash
python run_gui.py
# OR
python gui_app.py
```

---

## Troubleshooting Installation

### ❌ Problem: tkinter not found

**Windows:**
```bash
# Tkinter should be included, re-install Python with "tcl/tk and IDLE" checked
```

**macOS:**
```bash
# Install via Homebrew
brew install python-tk@3.9  # or your Python version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

### ❌ Problem: MediaPipe installation fails

```bash
# Try upgrading pip first
pip install --upgrade pip

# Then retry
pip install mediapipe
```

### ❌ Problem: TensorFlow is very large (>500MB)

```bash
# Use TensorFlow Lite Interpreter instead (smaller)
pip install --no-deps tflite-runtime
# Note: Adjust imports in code if using this
```

### ❌ Problem: OpenCV installation fails

```bash
# Try alternative installation
pip install opencv-python-headless
# For GUI, you need the full version, so:
pip uninstall opencv-python-headless
pip install opencv-python
```

### ❌ Problem: Camera not detected

```bash
# Check if camera is accessible
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"

# If False, try device 1, 2, etc.
```

---

## Verification Checklist

After installation, verify everything works:

```bash
# 1. Check Python version
python --version
# Expected: Python 3.8 or higher

# 2. Check all imports work
python -c "
import tkinter
import cv2
import mediapipe
import tensorflow
import numpy
from PIL import Image
print('✓ All imports successful')
"

# 3. Check camera access
python -c "
import cv2
cap = cv2.VideoCapture(0)
print('Camera accessible:', cap.isOpened())
cap.release()
"

# 4. Check models exist
import os
assert os.path.exists('model/keypoint_classifier/keypoint_classifier.tflite')
assert os.path.exists('model/point_history_classifier/point_history_classifier.tflite')
print('✓ All models found')

# 5. Run GUI
python run_gui.py
```

---

## System-Specific Notes

### Windows 10/11
- Generally most compatible
- May need to allow camera access through firewall
- Recommended: Visual C++ Runtime installed

### macOS
- Works well on M1/M2 (Apple Silicon)
- May need to grant camera permissions: System Preferences → Security & Privacy
- Requires Xcode command line tools: `xcode-select --install`

### Linux
- Ubuntu 18.04+ recommended
- May need to install camera drivers
- Flatpak/Snap packages may have sandbox restrictions

---

## Performance Optimization

### For Faster Inference:
1. **Use GPU acceleration**
   ```bash
   pip install tensorflow[and-cuda]  # NVIDIA GPU
   # For Apple Silicon: comes with optimized build
   ```

2. **Reduce resolution**
   - Edit `gui_config.py`: `VIDEO_WIDTH = 640`, `VIDEO_HEIGHT = 480`

3. **Lower detection confidence**
   - Edit `gui_config.py`: `MIN_DETECTION_CONFIDENCE = 0.5`

### For Better Memory Usage:
1. **Use TFLite interpreter only**
   - Don't load full TensorFlow

2. **Reduce history length**
   - Edit `gui_config.py`: `HISTORY_LENGTH = 8`

---

## IDE/Editor Recommendations

### VS Code
- Install Python extension
- Create `.venv` folder structure
- Set Python interpreter in workspace

### PyCharm Community Edition
- Configure project interpreter
- Install packages through IDE

### Command Line (Recommended)
- Simple and portable
- Works everywhere

---

## Creating Executable (Windows)

To create a standalone .exe file:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --icon=icon.ico gui_app.py

# .exe created in: dist/gui_app.exe
```

---

## Version Compatibility Matrix

| Component | Version | Status |
|-----------|---------|--------|
| Python | 3.8, 3.9, 3.10, 3.11 | ✓ Tested |
| MediaPipe | 0.8.1+ | ✓ Required |
| OpenCV | 3.4.2+ | ✓ Required |
| TensorFlow | 2.3.0+ | ✓ Required |
| NumPy | 1.19.0+ | ✓ Required |
| Pillow | 8.0.0+ | ✓ Required |

---

## File Size Reference

Expected disk usage after installation:

```
Python packages:
├─ tensorflow:      ~300-500 MB (largest)
├─ mediapipe:       ~100-150 MB
├─ opencv-python:   ~50-100 MB
├─ numpy:           ~50 MB
└─ other:           ~50 MB
                    ───────────
                    ~600-900 MB

Project models:
├─ keypoint_classifier.tflite:      ~200 KB
├─ point_history_classifier.tflite: ~100 KB
└─ training data:                   (variable)

Total Installation: ~700 MB - 1 GB
```

---

## Getting Help

If you encounter issues:

1. **Check logs**: Run `python run_gui.py` for error messages
2. **Check compatibility**: Verify Python and library versions
3. **Test components**: Use verification checklist above
4. **Check GUI_README.md**: For runtime troubleshooting
5. **Community**: Check GitHub issues

---

## Next Steps

After successful installation:

1. ✓ Run the GUI application
2. ✓ Test with your webcam
3. ✓ Collect training data (if needed)
4. ✓ Train custom models (see notebooks)
5. ✓ Integrate into your application

---

**Installation Guide Version**: 1.0  
**Last Updated**: April 2026  
**Support**: See GUI_README.md and GUI_QUICK_START.md
