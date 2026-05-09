# Real-Time Sign Language Recognition Using Pose Estimation and Vision Transformer

This repository contains a real-time sign language and hand gesture recognition system. It utilizes **MediaPipe** for accurate hand pose/keypoint estimation and a custom **Vision Transformer (ViT)** and **MLP** for classification. 

The project now features two ways to run the application:
1. **Local Desktop GUI:** Runs via Python and OpenCV (`app.py` or `gui_app.py`).
2. **Streamlit Web Application:** A web-ready version using WebRTC for real-time browser inference (`app_streamlit.py`).

![Demo](https://user-images.githubusercontent.com/37477845/102222442-c452cd00-3f26-11eb-93ec-c387c98231be.gif)

---

## 🌟 Key Features

- **Real-Time Hand Tracking:** Utilizes MediaPipe Hands to extract 21 3D landmarks of a hand from a single nn frame.
- **Vision Transformer (ViT) Classifier:** Includes a powerful Vision Transformer model implementation for robust keypoint classification.
- **Dynamic Finger Gesture Tracking:** Tracks the history of your index finger to recognize dynamic gestures (e.g., clockwise, counter-clockwise, moving).
- **Interactive Data Collection:** Built-in tools within the local GUI to collect your own hand gesture data and retrain the model.
- **WebRTC Integration:** Run the entire pipeline in your browser securely using `streamlit-webrtc`.

---

## 🛠️ Technology Stack

* **Computer Vision:** OpenCV (`cv2`), MediaPipe
* **Deep Learning:** TensorFlow/Keras (TFLite for inference), Vision Transformers (ViT)
* **Web Frontend:** Streamlit, Streamlit-WebRTC
* **Data Processing:** NumPy, Scikit-Learn, Pandas

---

## 🚀 Quick Start (Local Web App)

To run the Streamlit web application on your local machine:

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the Streamlit App:**
```bash
streamlit run app_streamlit.py
```
This will open `http://localhost:8501` in your browser. Grant webcam access when prompted, and start signing!

---

## 💻 Quick Start (Desktop GUI)

If you prefer to run the OpenCV window locally, bypassing the browser:

1. **Install GUI Dependencies:**
```bash
pip install -r requirements_gui.txt
```

2. **Run the App:**
```bash
python app.py
```
*(Press `ESC` to exit the window)*

---

## 🧠 Model Training & Customization

You can easily train the model on your own custom gestures using the provided Jupyter Notebooks.

### 1. Collect Data
Run `python app.py`. 
- Press `k` to enter "Keypoint Logging Mode". Press keys `0-9` to save current hand coordinates as that class ID. 
- Press `h` to enter "Point History Logging Mode" to save dynamic finger tracking.

### 2. Train the Model
Open the training notebooks and run them cell-by-cell to generate new `.tflite` models.
- **Static Hand Signs:** Use `keypoint_classification_vit.ipynb` (for Vision Transformer) or `keypoint_classification.ipynb` (for standard MLP).
- **Dynamic Gestures:** Use `point_history_classification.ipynb` (LSTM/MLP).

---

## 🌐 Deployment Guide (Cloud)

This repository is structured to be deployed easily to platforms like **Hugging Face Spaces** or **Streamlit Community Cloud**.

### Deploying to Hugging Face Spaces:
1. Create a free account on Hugging Face.
2. Create a new Space and choose **Streamlit** as your environment.
3. Upload the contents of this repository to your space.
4. Go to Settings -> **App file** and type `app_streamlit.py`.
5. Hugging Face will automatically install dependencies from `requirements.txt` and launch your app.

---

## 📁 Repository Structure

```text
├── app_streamlit.py                 # Main Streamlit web application
├── app.py                           # Local OpenCV application
├── requirements.txt                 # Dependencies for web deployment
├── requirements_gui.txt             # Dependencies for local GUI deployment
├── keypoint_classification_vit.ipynb # Vision Transformer training notebook
├── model/                           
│   ├── keypoint_classifier/         # Static sign models and label data
│   └── point_history_classifier/    # Dynamic gesture models and label data
└── utils/
    └── cvfpscalc.py                 # FPS measurement utility
```

---

## Acknowledgements
* Original base implementation and logic translated and adapted from Kazuhito Takahashi's hand gesture recognition system.
* Built using Google's [MediaPipe](https://mediapipe.dev/).
