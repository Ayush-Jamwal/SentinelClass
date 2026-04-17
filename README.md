# VisionSentinel AI: Adaptive Proctoring System

**VisionSentinel AI** is a real-time, computer-vision-based proctoring solution designed for academic and professional examinations. Utilizing **YOLOv8** for object detection and **DeepFace** for biometric verification, the system automates the detection of unauthorized materials and behaviors.

---

## 🌟 Key Features

* **Hex-Mode Matrix:** Six switchable security profiles (Strict, Open-Book, Digital, Open-Device, Group-Work, and Full-Collaboration).
* **Smart Hydration Grace Period:** Uses spatial math to detect bottles near the mouth, granting a 15s immunity to prevent false strikes during water breaks.
* **Anti-Vanish Lockdown:** Implements a penalty timer for Strike 3 violations. The timer automatically pauses if the student leaves the camera frame.
* **Forensic Evidence Logging:** Generates timestamped visual evidence of violations organized by student name and date.

---

## 🛠️ Technical Stack

* **Core:** Python 3.12
* **Object Detection:** YOLOv8 (S-model)
* **Facial Recognition:** DeepFace (VGG-Face weights)
* **UI & Alerts:** OpenCV, Tkinter, PyTTSx3 (Voice synthesis)
* **Hardware:** Optimized for NVIDIA CUDA-enabled GPUs

---

## 📂 Project Structure

```text
├── main.py                 # Main AI Execution Engine
├── known_faces/            # Student Biometric Database (Sample only)
├── .gitignore              # Privacy masking for biometric data
└── README.md               # Project Documentation