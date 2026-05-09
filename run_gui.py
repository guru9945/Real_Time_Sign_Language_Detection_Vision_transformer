#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick launcher for the Hand Gesture Recognition GUI
Run this file to start the interactive GUI application
"""

import os
import sys
from pathlib import Path

# Check if required files exist
def check_requirements():
    """Verify project structure and required files"""
    required_files = [
        'model/keypoint_classifier/keypoint_classifier.tflite',
        'model/keypoint_classifier/keypoint_classifier_label.csv',
        'model/point_history_classifier/point_history_classifier.tflite',
        'model/point_history_classifier/point_history_classifier_label.csv',
        'utils/cvfpscalc.py',
        'model/__init__.py'
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print("❌ Missing required files:")
        for file in missing:
            print(f"   - {file}")
        return False
    
    return True

# Check Python packages
def check_packages():
    """Verify required Python packages are installed"""
    required_packages = {
        'tkinter': 'tkinter (built-in)',
        'cv2': 'opencv-python',
        'mediapipe': 'mediapipe',
        'numpy': 'numpy',
        'tensorflow': 'tensorflow',
        'PIL': 'pillow'
    }
    
    missing = []
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing.append(pip_name)
    
    if missing:
        print("❌ Missing Python packages. Install with:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True

def main():
    print("=" * 60)
    print("  Hand Gesture Recognition GUI Launcher")
    print("=" * 60)
    
    # Check requirements
    print("\n📋 Checking project structure...")
    if not check_requirements():
        print("\n❌ Project structure incomplete!")
        return
    print("✓ All required files found")
    
    print("\n📦 Checking Python packages...")
    if not check_packages():
        print("\n❌ Please install missing packages and try again")
        return
    print("✓ All packages installed")
    
    print("\n" + "=" * 60)
    print("✓ All checks passed! Starting GUI...")
    print("=" * 60 + "\n")
    
    try:
        from gui_app import main as run_gui
        run_gui()
    except Exception as e:
        print(f"\n❌ Error starting GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
