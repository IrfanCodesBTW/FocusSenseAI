import cv2
import numpy as np
import csv
import os
from datetime import datetime
import time
from deepface import DeepFace

# ========================= CONFIG =========================
os.makedirs("data/raw_sessions", exist_ok=True)
HAAR_PATH = "haarcascade_frontalface_alt.xml"   # ← your file
HEAD_CENTER_THRESHOLD = 80   # pixels from center to be "focused"
LOG_INTERVAL = 1.0           # seconds
# =======================================================

face_cascade = cv2.CascadeClassifier(HAAR_PATH)

session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"data/raw_sessions/session_{session_id}.csv"

# Write header
with open(log_file, 'w', newline='') as f:
    csv.writer(f).writerow(['timestamp', 'focus_state', 'emotion', 'confidence'])

cap = cv2.VideoCapture(0)
last_log = time.time()
focus_history = []
last_emotion = "NEUTRAL"
last_conf = 0.0

print("FocusSense AI started!")
print("Look at the camera. Press Q to stop.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        state = "NO_FACE"
        emotion_text = "NO_FACE"
        conf = 0.0
    else:
        # Take the largest face
        (x, y, w, h) = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)[0]
        
        # Focus logic: is face near center of screen?
        face_center_x = x + w // 2
        frame_center_x = frame.shape[1] // 2
        if abs(face_center_x - frame_center_x) < HEAD_CENTER_THRESHOLD:
            state = "FOCUSED"
        else:
            state = "DISTRACTED"

        # Emotion
        try:
            emotions_result = DeepFace.analyze(frame[y:y+h, x:x+w], actions=['emotion'], enforce_detection=False, silent=True)
            if emotions_result:
                emotion_dict = emotions_result[0]['emotion']
                dom = max(emotion_dict, key=emotion_dict.get)
                conf = emotion_dict[dom] / 100.0  # normalize to 0-1
                mapping = {
                    'happy': 'HAPPY', 'surprise': 'HAPPY',
                    'angry': 'STRESSED', 'fear': 'STRESSED', 'disgust': 'STRESSED',
                    'sad': 'SLEEPY', 'neutral': 'NEUTRAL'
                }
                last_emotion = mapping.get(dom, 'NEUTRAL')
                last_conf = conf
        except:
            pass

        emotion_text = f"{last_emotion} ({last_conf:.2f})"

        # Draw
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0) if state == "FOCUSED" else (0, 0, 255), 3)

    # Smoothing focus state
    focus_history.append(state)
    if len(focus_history) > 5:
        focus_history.pop(0)
    current_focus = max(set(focus_history), key=focus_history.count)

    # Display on screen
    color = (0, 255, 0) if current_focus == "FOCUSED" else (0, 0, 255)
    cv2.putText(frame, f"Focus: {current_focus}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
    cv2.putText(frame, f"Emotion: {emotion_text}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("FocusSense AI - Press Q to stop", frame)

    # Log every second
    if time.time() - last_log >= LOG_INTERVAL:
        with open(log_file, 'a', newline='') as f:
            csv.writer(f).writerow([datetime.now().isoformat(), current_focus, last_emotion, last_conf])
        print(f"LOGGED → {current_focus} | {last_emotion}")
        last_log = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"Session saved → {log_file}")
