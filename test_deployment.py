#!/usr/bin/env python3
"""
Simple Deployment Test Script
Tests your system configuration and runs diagnostics
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

class DeploymentTester:
    def __init__(self):
        self.results = []
        self.system = platform.system()
    
    def test_python(self):
        """Test Python version"""
        print("Testing Python...", end=" ")
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            print(f"✓ Python {version.major}.{version.minor}")
            self.results.append(("Python", "✓"))
            return True
        else:
            print(f"✗ Python {version.major}.{version.minor} (Need 3.8+)")
            self.results.append(("Python", "✗"))
            return False
    
    def test_pip(self):
        """Test pip installation"""
        print("Testing pip...", end=" ")
        try:
            subprocess.run(["pip", "--version"], capture_output=True, check=True)
            print("✓ pip installed")
            self.results.append(("pip", "✓"))
            return True
        except:
            print("✗ pip not found")
            self.results.append(("pip", "✗"))
            return False
    
    def test_opencv(self):
        """Test OpenCV installation"""
        print("Testing OpenCV...", end=" ")
        try:
            import cv2
            print(f"✓ OpenCV {cv2.__version__}")
            self.results.append(("OpenCV", "✓"))
            return True
        except ImportError:
            print("✗ Not installed")
            self.results.append(("OpenCV", "✗"))
            return False
    
    def test_tensorflow(self):
        """Test TensorFlow installation"""
        print("Testing TensorFlow...", end=" ")
        try:
            import tensorflow as tf
            print(f"✓ TensorFlow {tf.__version__}")
            self.results.append(("TensorFlow", "✓"))
            return True
        except ImportError:
            print("✗ Not installed")
            self.results.append(("TensorFlow", "✗"))
            return False
    
    def test_mediapipe(self):
        """Test MediaPipe installation"""
        print("Testing MediaPipe...", end=" ")
        try:
            import mediapipe as mp
            print(f"✓ MediaPipe installed")
            self.results.append(("MediaPipe", "✓"))
            return True
        except ImportError:
            print("✗ Not installed")
            self.results.append(("MediaPipe", "✗"))
            return False
    
    def test_model_files(self):
        """Test model files exist"""
        print("Testing model files...", end=" ")
        model_path = Path("model/keypoint_classifier/keypoint_classifier_vit.tflite")
        label_path = Path("model/keypoint_classifier/keypoint_classifier_label.csv")
        
        if model_path.exists() and label_path.exists():
            model_size = model_path.stat().st_size / (1024*1024)
            print(f"✓ Model ({model_size:.1f}MB)")
            self.results.append(("Model Files", "✓"))
            return True
        else:
            print("✗ Not found")
            self.results.append(("Model Files", "✗"))
            return False
    
    def test_camera(self):
        """Test camera access"""
        print("Testing camera...", end=" ")
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                if ret:
                    print(f"✓ Camera accessible")
                    self.results.append(("Camera", "✓"))
                    return True
            print("✗ Cannot access camera")
            self.results.append(("Camera", "✗"))
            return False
        except Exception as e:
            print(f"✗ Error: {e}")
            self.results.append(("Camera", "✗"))
            return False
    
    def test_disk_space(self):
        """Test available disk space"""
        print("Testing disk space...", end=" ")
        import shutil
        total, used, free = shutil.disk_usage("/")
        free_gb = free / (1024*1024*1024)
        
        if free_gb > 2:
            print(f"✓ {free_gb:.1f}GB free")
            self.results.append(("Disk Space", "✓"))
            return True
        else:
            print(f"⚠ {free_gb:.1f}GB (Need 2GB+)")
            self.results.append(("Disk Space", "⚠"))
            return True  # Not critical
    
    def test_gpu(self):
        """Test GPU availability"""
        print("Testing GPU...", end=" ")
        try:
            import tensorflow as tf
            gpus = tf.config.list_physical_devices('GPU')
            if gpus:
                print(f"✓ {len(gpus)} GPU(s) found")
                self.results.append(("GPU", "✓"))
                return True
            else:
                print("ℹ CPU only (slower but functional)")
                self.results.append(("GPU", "ℹ"))
                return True
        except:
            print("ℹ CPU only")
            self.results.append(("GPU", "ℹ"))
            return True
    
    def test_web_framework(self):
        """Test Flask installation"""
        print("Testing Flask...", end=" ")
        try:
            import flask
            print(f"✓ Flask {flask.__version__}")
            self.results.append(("Flask", "✓"))
            return True
        except ImportError:
            print("⚠ Not installed (optional)")
            self.results.append(("Flask", "⚠"))
            return True
    
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 50)
        print("DEPLOYMENT READINESS TEST")
        print("=" * 50)
        print()
        
        self.test_python()
        self.test_pip()
        self.test_opencv()
        self.test_tensorflow()
        self.test_mediapipe()
        self.test_model_files()
        self.test_camera()
        self.test_disk_space()
        self.test_gpu()
        self.test_web_framework()
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print()
        print("=" * 50)
        print("TEST RESULTS SUMMARY")
        print("=" * 50)
        
        for test, result in self.results:
            status_icon = "✓" if result == "✓" else "✗" if result == "✗" else "ℹ"
            print(f"{status_icon} {test:20} {result:15}")
        
        print()
        print("=" * 50)
        
        # Count results
        passed = sum(1 for _, r in self.results if r == "✓")
        failed = sum(1 for _, r in self.results if r == "✗")
        
        if failed == 0:
            print(f"✓ ALL TESTS PASSED ({passed}/{len(self.results)})")
            print()
            print("Your system is ready for deployment!")
            print()
            print("Next steps:")
            print("1. Run: python gui_app.py       (for desktop)")
            print("2. Run: python web_app.py       (for web)")
            print("3. Run: deploy_windows.bat      (for guided setup)")
            return True
        else:
            print(f"✗ SOME TESTS FAILED ({passed}/{len(self.results)} passed)")
            print()
            print("Failed tests need fixing before deployment!")
            print()
            print("Install missing packages:")
            print("pip install -r requirements_deployment.txt")
            return False

def install_missing_packages():
    """Interactive package installation"""
    print()
    response = input("Would you like to auto-install missing packages? (y/n): ")
    
    if response.lower() == 'y':
        print("Installing packages...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements_deployment.txt"
        ])
        print("Installation complete! Re-run tests...")
        return True
    return False

def main():
    print()
    print("╔════════════════════════════════════════════════╗")
    print("║  Sign Language Detection - Deployment Tester  ║")
    print("╚════════════════════════════════════════════════╝")
    print()
    
    tester = DeploymentTester()
    success = tester.run_all_tests()
    
    if not success:
        if install_missing_packages():
            # Re-run tests
            print()
            print("Re-running tests...")
            print()
            tester2 = DeploymentTester()
            tester2.run_all_tests()
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
