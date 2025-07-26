from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import time
import random

app = Flask(__name__)
cap = cv2.VideoCapture(0)

moves = ["ROCK", "PAPER", "SCISSORS"]

user_score = 0
comp_score = 0

# Constants for finger landmarks
THUMB_TIP = 4
THUMB_IP = 3
INDEX_PIP = 6
INDEX_TIP = 8
MIDDLE_PIP = 10
MIDDLE_TIP = 12
RING_PIP = 14
RING_TIP = 16
PINKY_PIP = 18
PINKY_TIP = 20

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def detect_gesture(landmarks, handedness):
    if handedness == "Right":
        thumb = landmarks[THUMB_TIP].x < landmarks[THUMB_IP].x
    else:
        thumb = landmarks[THUMB_TIP].x > landmarks[THUMB_IP].x
    index = landmarks[INDEX_PIP].y > landmarks[INDEX_TIP].y
    middle = landmarks[MIDDLE_PIP].y > landmarks[MIDDLE_TIP].y
    ring = landmarks[RING_PIP].y > landmarks[RING_TIP].y
    pinky = landmarks[PINKY_PIP].y > landmarks[PINKY_TIP].y

    if thumb and index and middle and ring and pinky:
        return "PAPER"
    elif not thumb and index and middle and not ring and not pinky:
        return "SCISSORS"
    elif not thumb and not index and not middle and not ring and not pinky:
        return "ROCK"
    else:
        return "INVALID"

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        label = ""
        if result.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                handedness = result.multi_handedness[idx].classification[0].label
                label = detect_gesture(hand_landmarks.landmark, handedness)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('MediaPipe Hands', frame)
        
        # if label:
        #     cv2.putText(frame, label, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html', move=None)

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/play')
def play():
    global user_score, comp_score 
    success, frame = cap.read()
    if not success:
        return jsonify({'error': 'Camera read failed'})

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    user_move = "INVALID"
    if result.multi_hand_landmarks and result.multi_handedness:
        hand_landmarks = result.multi_hand_landmarks[0]
        handedness = result.multi_handedness[0].classification[0].label
        user_move = detect_gesture(hand_landmarks.landmark, handedness)

    comp_move = random.choice(moves)

    if user_move not in moves:
        result_text = "Could not detect your move"
    elif comp_move == user_move:
        result_text = "IT'S A TIE"
    elif (comp_move == "ROCK" and user_move == "SCISSORS") or \
         (comp_move == "SCISSORS" and user_move == "PAPER") or \
         (comp_move == "PAPER" and user_move == "ROCK"):
        result_text = "YOU LOSE"
        comp_score += 1
    else:
        result_text = "YOU WIN"
        user_score += 1

    return jsonify({
        'move': comp_move,
        'user': user_move,
        'result': result_text,
        'user_score': user_score,
        'comp_score': comp_score
    })


if __name__ == '__main__':
    user_score = 0
    comp_score = 0
    app.run(debug=True)

