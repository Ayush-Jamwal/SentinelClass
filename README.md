# VisionSentinel AI 🛡️
### Adaptive Computer-Vision Proctoring System

**VisionSentinel AI** is a professional-grade automated proctoring solution developed to ensure academic integrity. It combines real-time object detection (**YOLOv8**) with biometric identification (**DeepFace**) to create a dynamic "Rainbow of Security."

---

## 🚀 Innovative Features

### 1. Hex-Mode Adaptive Logic
Switch between 6 distinct security protocols in real-time using keyboard interrupts (0-5):
* **Strict Omni-Vision:** Zero-tolerance monitoring.
* **Paper Open-Book:** Allows books but blocks devices.
* **Digital Exam:** Permits laptops but flags mobile devices.
* **Group Work:** Disables proximity/whisper detection.
* ...and more.

### 2. Intelligent Hydration Grace
Using Euclidean distance calculations, the system detects when a water bottle is near a student's mouth. It automatically grants a **15-second "Hydration Grace,"** preventing false strikes for looking away or being obscured while drinking.

### 3. Anti-Vanish Lockdown Security
If a student reaches **Strike 3** or leaves the room (**Unauthorized Exit**), they enter a **5-minute Lockdown**. The penalty timer is "Smart"—it pauses if the student is not in the frame, ensuring the penalty is only served while they are under supervision.

### 4. Forensic Evidence Suite
Automatically organizes photographic evidence of violations into a date-structured directory:
`evidence/[Student_Name]/[YYYY-MM-DD]/STRIKE_X.jpg`

---

## 🛠️ Technical Implementation
* **Language:** Python 3.12
* **Vision Models:** YOLOv8 (S-Variant), VGG-Face via DeepFace.
* **Alert Systems:** * **OS:** Tkinter Modal Popups.
    * **Audio:** PyTTSx3 Voice Synthesis & Winsound Beeps.
    * **Cloud:** Twilio API Scaffolding (Optional SMS).
* **Privacy:** Implements `.gitignore` biometric masking to prevent private data leakage.

---

## 📂 Project Structure

```text
├── main.py                 # Main AI Execution Engine
├── known_faces/            # Student Biometric Database (Sample only)
├── .gitignore              # Privacy masking for biometric data
└── README.md               # Project Documentation

---

## ⚖️ License
Distributed under the **MIT License**. Created for Engineering Seminar 2026.