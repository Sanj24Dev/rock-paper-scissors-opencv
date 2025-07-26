# 🤘 Rock-Paper-Scissors with Hand Gesture Recognition (Flask + MediaPipe + OpenCV)

This project is a real-time Rock-Paper-Scissors game that uses your webcam to detect hand gestures using [MediaPipe](https://google.github.io/mediapipe/) and plays against a computer opponent. It is built using **Flask** for the web server and **OpenCV** for video capture.

## 📁 Project Structure
├── app.py                                   # Main Flask application <br>
├── img_detection.py                         # Standalone test script for gesture detection <br>
├── templates/ <br>
&nbsp;&nbsp;&nbsp;&nbsp;└── index.html       # Frontend HTML file served by Flask <br>
├── static/ <br>
&nbsp;&nbsp;&nbsp;&nbsp;├── rock.png         # Image shown for computer's "Rock" move <br>
&nbsp;&nbsp;&nbsp;&nbsp;├── paper.png        # Image shown for "Paper" <br>
&nbsp;&nbsp;&nbsp;&nbsp;├── scissors.png     # Image shown for "Scissors" <br>
&nbsp;&nbsp;&nbsp;&nbsp;└── question.png     # Placeholder image <br>
└── requirements.txt                         # File for installing dependencies <br>


## 🚀 Features

- Real-time webcam feed in browser
- Detects hand gestures: ✊ Rock, ✋ Paper, ✌️ Scissors
- Displays animated countdown before capturing move
- Keeps track of user vs computer scores
- Fully client-server architecture using Flask

## 🎮 How to Play

1. **Clone this repository and move into the folder**
   ```bash
   git clone https://github.com/Sanj24Dev/rock-paper-scissors-opencv.git
   cd rock-paper-scissors-opencv
2. **Install the requiremnts**
   ```bash
   pip install -r requirements.txt
3. **Start the server**:
   ```bash
   python app.py
4. **Open your browser and go to:**
    http://127.0.0.1:5000

5. **Show your move (Rock, Paper, or Scissors) in front of the webcam.**

6. **Click "PLAY" and wait for the result after the "ROCK . . PAPER . . SCISSORS . . Shoot!"**

## 🧠 Gesture Detection Logic
The system uses finger landmark positions from MediaPipe Hands to classify gestures as:

* ROCK: All fingers closed
* PAPER: All fingers extended
* SCISSORS: Only index and middle fingers extended

## 🔧 Dependencies
* Python 3.x
* Flask
* OpenCV
* MediaPipe
* keyboard (only used in img_detection.py for testing)

Install dependencies using pip:

bash
Copy
Edit
pip install flask opencv-python mediapipe keyboard

## 📝 Notes
* Webcam access is required.
* Tested on Chrome and Firefox.
* For best results, show your gesture clearly in front of the camera.

## 📷 Demo
