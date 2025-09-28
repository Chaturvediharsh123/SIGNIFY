✨ Signfy ✨


Signfy is a real-time Sign Language to Speech converter that bridges communication gaps between hearing-impaired individuals and others by translating hand gestures into audible speech.

🚀 Features

🖐️ Real-time hand gesture recognition using MediaPipe

🗣️ Converts recognized signs into speech using pyttsx3

💻 Optional Streamlit GUI for easy interaction

⚡ Lightweight and works on standard laptops with webcam

🎯 Can be extended to support multiple languages and additional gestures

🛠️ Tech Stack

Python 3.x

OpenCV – for video capture and processing

MediaPipe – for hand landmark detection

NumPy – for data handling and calculations

pyttsx3 – text-to-speech conversion

Streamlit (optional) – web-based interface

📂 Installation

Clone the repository:

git clone https://github.com/Chaturvediharsh123/signfy.git
cd signfy


Install dependencies:

pip install -r requirements.txt

▶️ Usage

Run the app:

python app.py


Or with Streamlit interface:

streamlit run multi.py


How it works:

Webcam captures hand gestures in real-time

MediaPipe detects key hand landmarks

Classifier predicts the corresponding sign

pyttsx3 converts recognized signs into speech

📦 Requirements
opencv-python
mediapipe
numpy
pyttsx3
streamlit
protobuf==3.20.*

🧠 How it Works

Hand Detection: MediaPipe identifies hand landmarks from webcam feed.

Sign Classification: Positions of fingers and hand gestures are analyzed to classify signs.

Speech Conversion: Recognized signs are converted to speech using pyttsx3.

✨ Inspiration

Signfy was created to enhance communication accessibility for hearing-impaired individuals. It demonstrates how AI and computer vision can bridge communication gaps and make everyday interactions easier.

🤝 Contributing

Contributions are welcome! Ideas for improvement:

Add more gestures to the classifier

Multi-language support for speech

Optimize real-time performance

📜 License

This project is licensed under the MIT License.
