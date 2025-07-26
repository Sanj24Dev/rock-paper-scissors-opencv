import cv2
import mediapipe as mp
import keyboard  
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

THUMB_FINGER_TIP_ID = 4
THUMB_FINGER_IP_ID = 3
INDEX_FINGER_TIP_ID = 8
INDEX_FINGER_PIP_ID = 6
MIDDLE_FINGER_TIP_ID = 12
MIDDLE_FINGER_PIP_ID = 10
RING_FINGER_TIP_ID = 16
RING_FINGER_PIP_ID = 14
PINKY_FINGER_TIP_ID = 20
PINKY_FINGER_PIP_ID = 18

debounce_delay = 0.2

def read_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark
    thumb_up = landmarks[THUMB_FINGER_TIP_ID].x < landmarks[THUMB_FINGER_IP_ID].x
    index_up = landmarks[INDEX_FINGER_PIP_ID].y > landmarks[INDEX_FINGER_TIP_ID].y
    middle_up = landmarks[MIDDLE_FINGER_PIP_ID].y > landmarks[MIDDLE_FINGER_TIP_ID].y
    ring_up = landmarks[RING_FINGER_PIP_ID].y > landmarks[RING_FINGER_TIP_ID].y
    pinky_up = landmarks[PINKY_FINGER_PIP_ID].y > landmarks[PINKY_FINGER_TIP_ID].y

    if thumb_up and index_up and middle_up and ring_up and pinky_up:
        print("PAPER")
    elif not thumb_up and index_up and middle_up and not ring_up and not pinky_up:
        print("SCISSORS")
    elif not thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
        print("ROCK")
    else:
        print("INVALID MOVE")

def main():
    last_pressed = time.time()
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Only run gesture check if Enter key is pressed
                    if keyboard.is_pressed('enter'):
                        # handling debounce of the key to avoid multiple presses
                        current_time = time.time()
                        if current_time - last_pressed > debounce_delay:
                            read_gesture(hand_landmarks)
                            last_pressed = current_time


                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:  # ESC to exit
                break
    cap.release()

if __name__ == "__main__":
    main()
