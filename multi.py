import cv2
import mediapipe as mp
import pyttsx3
import numpy as np
from collections import deque, Counter

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)  # max_num_hands=2 to detect both hands
mp_draw = mp.solutions.drawing_utils

# Initialize speech engine
engine = pyttsx3.init()

# Extract landmarks from hand
def get_landmarks(hand_landmarks):
    return np.array([[lm.x, lm.y] for lm in hand_landmarks.landmark])

# Rule-based recognizer for 10 common signs (can apply per hand)
def recognize_sign(landmarks):
    index_tip, middle_tip, ring_tip, pinky_tip = landmarks[8], landmarks[12], landmarks[16], landmarks[20]
    index_dip, middle_dip, ring_dip, pinky_dip = landmarks[7], landmarks[11], landmarks[15], landmarks[19]
    thumb_tip, thumb_ip = landmarks[4], landmarks[3]

    # Hello → all fingers up
    if (index_tip[1] < index_dip[1] and middle_tip[1] < middle_dip[1] and
        ring_tip[1] < ring_dip[1] and pinky_tip[1] < pinky_dip[1]):
        return "hello"
    # Yes → fist
    elif (index_tip[1] > index_dip[1] and middle_tip[1] > middle_dip[1] and
          ring_tip[1] > ring_dip[1] and pinky_tip[1] > pinky_dip[1]):
        return "yes"
    # No → index + middle up
    elif (index_tip[1] < index_dip[1] and middle_tip[1] < middle_dip[1] and
          ring_tip[1] > ring_dip[1] and pinky_tip[1] > pinky_dip[1]):
        return "no"
    # Love → index + pinky up
    elif (index_tip[1] < index_dip[1] and pinky_tip[1] < pinky_dip[1] and
          middle_tip[1] > middle_dip[1] and ring_tip[1] > ring_dip[1]):
        return "love"
    # Stop → all fingers up + thumb sideways
    elif (index_tip[1] < index_dip[1] and middle_tip[1] < middle_dip[1] and
          ring_tip[1] < ring_dip[1] and pinky_tip[1] < pinky_dip[1] and
          thumb_tip[0] < thumb_ip[0]):
        return "stop"
    # Thank you → flat hand forward
    elif (index_tip[1] < index_dip[1] and middle_tip[1] < middle_dip[1] and
          ring_tip[1] < ring_dip[1] and pinky_tip[1] < pinky_dip[1] and
          thumb_tip[1] < thumb_ip[1]):
        return "thank you"
   
   
    # Rock → index + pinky up, middle + ring down
    elif (index_tip[1] < index_dip[1] and pinky_tip[1] < pinky_dip[1] and
          middle_tip[1] > middle_dip[1] and ring_tip[1] > ring_dip[1]):
        return "rock"
    #point 
    elif index_tip[1] < index_dip[1] and middle_tip[1] > middle_dip[1] \
         and ring_tip[1] > ring_dip[1] and pinky_tip[1] > pinky_dip[1]:
        return "point"
    # Thumb up → only thumb up
    elif (thumb_tip[1] < thumb_ip[1] and index_tip[1] > index_dip[1]):
        return "thumbs up"
    #finger gun
    elif index_tip[1] < index_dip[1] and thumb_tip[1] < thumb_ip[1] \
         and middle_tip[1] > middle_dip[1] and ring_tip[1] > ring_dip[1] \
         and pinky_tip[1] > pinky_dip[1]:
        return "finger gun"
    # Call me 🤙 → thumb + pinky up
    elif (thumb_tip[1] < thumb_ip[1] and pinky_tip[1] < pinky_dip[1] and
          index_tip[1] > index_dip[1] and middle_tip[1] > middle_dip[1] and
          ring_tip[1] > ring_dip[1]):
        return "call me"
     # Victory ✌️ → peace sign (already covered, but you can differentiate angle if needed)
    elif (index_tip[1] < index_dip[1] and middle_tip[1] < middle_dip[1] and
          ring_tip[1] > ring_dip[1] and pinky_tip[1] > pinky_dip[1] and
          abs(index_tip[0] - middle_tip[0]) > 0.05):
        return "victory"
    

     # Numbers 1–5
    elif (index_tip[1] < index_dip[1] and middle_tip[1] > middle_dip[1] and
          ring_tip[1] > ring_dip[1] and pinky_tip[1] > pinky_dip[1]):
        return "1"
    elif (index_tip[1] < index_dip[1] and middle_tip[1] < middle_dip[1] and
          ring_tip[1] > ring_dip[1] and pinky_tip[1] > pinky_dip[1]):
        return "2"
    elif (index_tip[1] < index_dip[1] and middle_tip[1] < middle_dip[1] and
          ring_tip[1] < ring_dip[1] and pinky_tip[1] > pinky_dip[1]):
        return "3"
    elif (index_tip[1] < index_dip[1] and middle_tip[1] < middle_dip[1] and
          ring_tip[1] < ring_dip[1] and pinky_tip[1] < pinky_dip[1] and
          thumb_tip[1] > thumb_ip[1]):
        return "4"
    elif (index_tip[1] < index_dip[1] and middle_tip[1] < middle_dip[1] and
          ring_tip[1] < ring_dip[1] and pinky_tip[1] < pinky_dip[1] and
          thumb_tip[1] < thumb_ip[1]):
        return "5"
    elif (all([index_tip[1] < index_dip[1], middle_tip[1] < middle_dip[1],
               ring_tip[1] < ring_dip[1], pinky_tip[1] < pinky_dip[1]])):
        return "clap"
    else:
        return None

# Moving window for smoothing predictions
WINDOW_SIZE = 5
predictions = deque(maxlen=WINDOW_SIZE)
last_spoken = None

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # For both hands, collect predictions
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = get_landmarks(hand_landmarks)
            sign = recognize_sign(landmarks)
            predictions.append(sign)

    # Smooth prediction using majority vote
    if len(predictions) == WINDOW_SIZE:
        most_common = Counter(predictions).most_common(1)[0][0]
        if most_common and most_common != last_spoken:
            last_spoken = most_common
            engine.say(most_common)
            engine.runAndWait()
        if most_common:
            cv2.putText(frame, most_common, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2)

    cv2.imshow("Sign to Speech (Both Hands)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
