SIGNIFY: REAL TIME SIGN LANGUAGE TO SPEECH🖐️🔊

This project uses AI and computer vision to detect sign language gestures in real-time and convert them into spoken words. The system leverages Mediapipe for hand tracking, a gesture classification model, and text-to-speech engines (pyttsx3 / gTTS / edge-tts) to enable seamless communication.

📌 Features

✅ Real-time sign language gesture detection (ASL / custom gestures)
✅ Gesture-to-speech conversion with AI-powered text-to-speech
✅ Works on images, webcam video feeds, and recorded videos
✅ Fast and accurate recognition for everyday communication
✅ Output displays gesture name and spoken word in real-time

🛠️ Tech Stack

🐍 Python 3
🎥 OpenCV – real-time video capture and processing
✋ Mediapipe – hand landmark detection
🤖 TensorFlow / PyTorch – gesture classification
🔊 pyttsx3 / gTTS / edge-tts – text-to-speech conversion
☁️ Google Colab – run without local setup

📂 Project Structure
Signify-Sign-to-Speech/
│
├── weights/
│   ├── gesture_model.pt       # Trained gesture classification model
├── main.py                    # Python script to run the application
├── demo_image.jpg             # Sample input image for testing
├── demo_video.mp4             # Sample video input (optional)
├── app.ipynb                  # Google Colab notebook
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation

2️⃣ Install Dependencies

Make sure you are inside the project folder, then install dependencies:

cd Signify-Sign-to-Speech
pip install -r requirements.txt
