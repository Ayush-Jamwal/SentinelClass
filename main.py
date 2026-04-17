import os
import cv2
import numpy as np
from deepface import DeepFace
from ultralytics import YOLO
import time
import datetime
import pyttsx3
import winsound
import math 
import torch
import tkinter as tk
from tkinter import messagebox

# Hide TensorFlow warnings for a cleaner console
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

# ==========================================================
# 0. SYSTEM CONFIGURATION & ALERTS
# ==========================================================
device = 'cuda' if torch.cuda.is_available() else 'cpu'
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def send_remote_alert(name, reason):
    """Optional Twilio SMS Logic - Uses Env Vars for Security"""
    try:
        from twilio.rest import Client
        sid = os.getenv('TWILIO_ACCOUNT_SID')
        token = os.getenv('TWILIO_AUTH_TOKEN')
        if sid and token:
            client = Client(sid, token)
            client.messages.create(
                body=f"SENTINEL LOCKDOWN: {name} flagged for {reason}.",
                from_='+1234567890', # Placeholder
                to='+91XXXXXXXXXX'    # Placeholder
            )
            print(f"📱 SMS Alert Sent for {name}")
    except: pass # Silent skip if Twilio is not configured

def trigger_violation(name, strike, reason):
    """Triggers Audio, Visual, and OS-level alerts"""
    print(f"⚠️ VIOLATION: {name} | Strike {strike} | Reason: {reason}")
    winsound.Beep(1000, 400) 
    engine.say(f"Violation. {name}, {reason}.")
    engine.runAndWait()
    
    if strike >= 3:
        send_remote_alert(name, reason)
        root = tk.Tk(); root.withdraw(); root.attributes("-topmost", True)
        messagebox.showwarning("SENTINEL LOCKDOWN", f"Student {name} is locked for 5 minutes.")
        root.destroy()

# ==========================================================
# 1. AI MODELS & DATABASE INITIALIZATION
# ==========================================================
model = YOLO('yolov8s.pt').to(device)
db_path = "known_faces"    
student_trackers = {}  
STRIKE_COOLDOWN = 10 
PROBATION_TIME = 300 # 5 Minutes

# THE ADAPTIVE 6-MODE MATRIX
SYSTEM_MODES = {
    ord('0'): {"name": "STRICT OMNI-VISION", "look_away": False, "phone": False, "laptop": False, "whisper": False, "color": (0, 255, 255)},
    ord('1'): {"name": "PAPER OPEN-BOOK",   "look_away": True,  "phone": False, "laptop": False, "whisper": False, "color": (0, 165, 255)},
    ord('2'): {"name": "DIGITAL EXAM",     "look_away": True,  "phone": False, "laptop": True,  "whisper": False, "color": (255, 100, 100)},
    ord('3'): {"name": "OPEN DEVICE",      "look_away": True,  "phone": True,  "laptop": True,  "whisper": False, "color": (100, 255, 100)},
    ord('4'): {"name": "GROUP WORK",       "look_away": True,  "phone": False, "laptop": False, "whisper": True,  "color": (255, 100, 255)},
    ord('5'): {"name": "FULL COLLABORATION","look_away": True,  "phone": True,  "laptop": True,  "whisper": True,  "color": (255, 255, 255)},
}
current_mode_key = ord('0')

cap = cv2.VideoCapture(0)
cv2.namedWindow("SentinelClass AI - Master Final")

# ==========================================================
# 2. MAIN PROCESSING LOOP
# ==========================================================
while True:
    ret, frame = cap.read()
    if not ret: break

    now = time.time()
    active_mode = SYSTEM_MODES[current_mode_key]
    active_phones, active_laptops, active_books, active_bottles, active_faces = [], [], [], [], {}

    # --- 2.1 YOLO DETECTION (Multi-Object Logic) ---
    results_yolo = model.predict(frame, classes=[0, 39, 63, 67, 73], conf=0.25, verbose=False)
    for r in results_yolo:
        for box in r.boxes:
            cls, conf, (x1, y1, x2, y2) = int(box.cls[0]), float(box.conf[0]), map(int, box.xyxy[0])
            
            if cls == 67 and conf > 0.40: # Phone (Red)
                active_phones.append((x1, y1, x2, y2))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            elif cls == 63: # Laptop (Purple)
                active_laptops.append((x1, y1, x2, y2))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (128, 0, 128), 3)
            elif cls == 73: # Books (Blue)
                active_books.append((x1, y1, x2, y2))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            elif cls == 39: # Bottle (Orange)
                active_bottles.append((x1, y1, x2, y2))

    # --- 2.2 DEEPFACE BIOMETRICS (Identity Logic) ---
    try:
        results = DeepFace.find(img_path=frame, db_path=db_path, model_name='VGG-Face', enforce_detection=False, silent=True)
        for face_data in results:
            if not face_data.empty:
                name = os.path.basename(face_data['identity'].iloc[0]).split('.')[0]
                x, y, w, h = map(int, [face_data['source_x'].iloc[0], face_data['source_y'].iloc[0], face_data['source_w'].iloc[0], face_data['source_h'].iloc[0]])
                active_faces[name] = (x, y, x+w, y+h)
                
                if name not in student_trackers:
                    student_trackers[name] = {"strikes": 0, "last_seen": now, "last_strike": 0, "drink_grace": 0, "phone_start": 0, "probation_end": 0}
                
                student_trackers[name]["last_seen"] = now
                color = (0, 0, 255) if now < student_trackers[name]["probation_end"] else (0, 255, 0)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, f"{name} ({student_trackers[name]['strikes']}/3)", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    except: pass

    # ==========================================================
    # 3. THE MASTER JUDGE ENGINE
    # ==========================================================
    for name, data in student_trackers.items():
        violation = None
        
        # --- 3.1 LOCKDOWN SECURITY ---
        if data["probation_end"] > now:
            if name not in active_faces:
                data["probation_end"] += 0.1 # Pause penalty if they leave
                cv2.putText(frame, "LOCKDOWN PAUSED: SUBJECT MISSING", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            else:
                fx1, fy1, fx2, fy2 = active_faces[name]
                cv2.putText(frame, f"PENALTY: {int(data['probation_end']-now)}s", (fx1, fy1-35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
            continue 
        elif data["probation_end"] != 0:
            data["strikes"], data["probation_end"] = 1, 0 # Reset to Strike 1 after probation

        # --- 3.2 SMART HYDRATION GRACE ---
        if name in active_faces:
            fx1, fy1, fx2, fy2 = active_faces[name]
            mouth_y = fy2 - ((fy2 - fy1) * 0.2) 
            for (bx1, by1, bx2, by2) in active_bottles:
                if math.sqrt(((fx1+fx2)/2 - (bx1+bx2)/2)**2 + (mouth_y - (by1+by2)/2)**2) < 150:
                    data["drink_grace"] = now + 15

        if now < data["drink_grace"]:
            data["last_seen"] = now 
            if name in active_faces:
                fx1, fy1, fx2, fy2 = active_faces[name]
                cv2.putText(frame, "HYDRATION GRACE", (fx1, fy1-35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
            continue

        # --- 3.3 VIOLATION DETECTION ---
        if name in active_faces:
            fx1, fy1, fx2, fy2 = active_faces[name]
            
            # Device Detection (with 5s Grace)
            phone_nearby = any(fx1-150 < (px1+px2)/2 < fx2+150 for px1,py1,px2,py2 in active_phones)
            if not active_mode["phone"] and phone_nearby:
                if data["phone_start"] == 0: data["phone_start"] = now
                if (now - data["phone_start"]) > 5: violation = "Device Usage"
                else: cv2.putText(frame, f"PHONE: {int(5-(now-data['phone_start']))}s", (fx1, fy2+30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
            else: data["phone_start"] = 0
            
            # Proximity/Whisper Detection
            if not active_mode["whisper"] and not violation:
                for oname, (ox1, oy1, ox2, oy2) in active_faces.items():
                    if oname != name and math.sqrt(((fx1+fx2)/2 - (ox1+ox2)/2)**2 + ((fy1+fy2)/2 - (oy1+oy2)/2)**2) < 150:
                        violation = "Suspicious Proximity"

        # --- 3.4 ABSENCE & EXIT LOGIC ---
        abs_dur = now - data["last_seen"]
        if abs_dur > 60: violation = "Unauthorized Exit"
        elif abs_dur > 5 and not active_mode["look_away"]:
            if len(active_books) == 0: violation = "Looking Away"

        # --- 3.5 FORENSIC RECORDING ---
        if violation and (now - data["last_strike"] > STRIKE_COOLDOWN):
            data["strikes"] = 3 if violation == "Unauthorized Exit" else data["strikes"] + 1
            if data["strikes"] >= 3: data["probation_end"] = now + PROBATION_TIME
            
            data["last_strike"] = now
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            folder = os.path.join("evidence", name, today); os.makedirs(folder, exist_ok=True)
            cv2.imwrite(os.path.join(folder, f"STRIKE_{data['strikes']}_{int(now)}.jpg"), frame)
            trigger_violation(name, data["strikes"], violation)

    # --- 4. HUD RENDER ---
    cv2.putText(frame, f"MODE: {active_mode['name']}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, active_mode['color'], 2)
    cv2.imshow("SentinelClass AI - Master Final", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key in [ord('q'), ord('Q')]: break
    elif key in SYSTEM_MODES: 
        current_mode_key = key
        engine.say(f"System switched to {SYSTEM_MODES[key]['name']}")
        engine.runAndWait()

cap.release(); cv2.destroyAllWindows()