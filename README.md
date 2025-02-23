

# 📚 Code Documentation: Real-Time Speech Translator

## 📌 Overview

This Flask-based application enables real-time speech-to-text conversion, translation, and text-to-speech synthesis to facilitate communication between patients and health workers in different languages.

## 🚀 Key Features

- **Speech Recognition**: Uses Google Cloud Speech-to-Text for transcribing speech.
- **Language Translation**: Uses Google Translate to convert transcriptions.
- **Text-to-Speech (TTS)**: Uses gTTS to generate spoken audio.
- **User Interface**: Provides an interactive web-based UI for recording and playing translated speech.
- **Security**: Implements logging, API key management, and input validation.

## 💂️ Security Considerations
- Uses **.env** file for storing credentials securely instead of hardcoding.
- Logs system activity for debugging.
- Implements input validation to prevent erroneous API calls.
- Enforces SSL encryption for secure connections.

## 📂 Project Structure

```
/project-directory
├── app.py
├── key
├── log
│   └── app.log
├── README.md
├── requirements.txt
├── static
│   ├── index.html
│   ├── languages.json
│   ├── script.js
│   └── styles.css
└── user-guide.md        
```

## 🛠️ Technology Stack

| Component             | Technology Used           |
|----------------------|--------------------------|
| Backend             | Flask (Python)            |
| Frontend            | HTML, CSS, JavaScript (AJAX) |
| Speech Recognition  | Google Cloud Speech-to-Text |
| Translation         | Google Translate API       |
| Text-to-Speech (TTS)| gTTS                      |





## 🌍 **Translation Options and Considerations**

For translation, **OpenAI API** or a **custom-trained LLM** can be utilized. Additionally, **FastText by Facebook** is a great alternative, especially for medical terminology and Indic languages. FastText offers robust multilingual support, making it highly suitable for specialized translations. However, due to the high computational power and cost associated with these solutions, they have not been implemented in this project.



## 🖥️ Flask Backend (app.py)

### 📌 Modules Used

```python
import os
import threading
import asyncio
from gtts import gTTS
from flask import Flask, request, jsonify, Response
from google.cloud import speech
from googletrans import Translator
from dotenv import load_dotenv
import logging
```

- **Flask** → Handles API requests.
- **gTTS** → Converts translated text into speech.
- **Google Cloud Speech-to-Text** → Recognizes spoken words.
- **Google Translate (googletrans)** → Translates recognized text.
- **Logging** → Captures system events for debugging.
- **Dotenv** → Loads API credentials securely.

### 🛠️ Flask App Initialization

```python
load_dotenv()

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

app = Flask(__name__)

# Logging Configuration
logging.basicConfig(filename='log/app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# Global variables for language selection
patientLan = None
workerLan = None
```

## 🛠️ API Endpoints

### 1️⃣ Home Route (/)

```python
@app.route('/')
def root():
    delete_all_audio_files()
    return app.send_static_file('index.html')
```
- Serves the frontend UI (index.html).

### 2️⃣ Speech-to-Text API (/mic-input)

```python
@app.route('/mic-input', methods=['POST'])
def mic_input():
    if 'file' not in request.files:
        app.logger.error('ERROR: No file provided')
        return jsonify({"error": "⚠️ No speech detected. Please try again."}), 400

    file = request.files['file']
    src_language = request.form.get('language')
    micId = request.form.get('button_id')

    transcript = transcribe_audio(file.read(), src_language)
    
    if transcript:
        app.logger.info(f'Transcription successful for {micId}: {transcript}')
        thread = threading.Thread(target=post_transcription_action, args=(transcript, src_language, micId))
        thread.start()
        return transcript
    else:
        delete_file_or_directory(micId)
        return jsonify({"error": "⚠️ No speech detected or language not recognized."}), 400
```
- Receives an audio file from the frontend.
- Uses `transcribe_audio()` to convert speech to text.
- Runs translation & text-to-speech in a background thread.

### 3️⃣ Speech Recognition (transcribe_audio())

```python
def transcribe_audio(file_data, src_language):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=file_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code=src_language
    )
    response = client.recognize(config=config, audio=audio)
    return ''.join([result.alternatives[0].transcript for result in response.results])
```
- Google Cloud Speech-to-Text API converts the audio to text.

### 4️⃣ Translation (translate_text())

```python
def translate_text(text, src_lang, tar_lang):
    try:
        translator = Translator()
        translation = asyncio.run(translator.translate(text, dest=tar_lang, src=src_lang))
        return translation.text
    except Exception as e:
        app.logger.error(f"Translation error: {e}")
        return None
```
- Uses Google Translate API for multilingual support.

### 5️⃣ Text-to-Speech (text_to_speech())

```python
def text_to_speech(text, filename, lang):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        return True
    except Exception as e:
        return False
```
- Converts translated text into an MP3 audio file.

### 6️⃣ Serve Audio (/play-audio)

```python
@app.route('/play-audio', methods=['POST'])
def play_audio():
    data = request.get_json()
    button_id = data.get('button_id')
    file_path = "./audio/patient.mp3" if button_id == "playTTSButton" else "./audio/healthworker.mp3"
    if os.path.exists(file_path):
        def generate():
            with open(file_path, "rb") as audio_file:
                yield from audio_file
        return Response(generate(), mimetype="audio/mp3")
    return jsonify({"error": "Audio file not found"}), 404
```
- Streams the translated speech audio for playback.

## 🌐 Deployment

### 🛠️ Install Dependencies

```sh
pip install flask google-cloud-speech googletrans gtts python-dotenv
```

### 🚀 Run Flask App

```sh
python app.py
```

### 🌐 Access the Web Interface

- Open `https://0.0.0.0:8080` in your browser.


