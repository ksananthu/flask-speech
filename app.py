import os
import threading
# import uuid
from flask import Flask, flash, request, redirect, jsonify # type: ignore
from google.cloud import speech
from googletrans import Translator
import logging

# https://github.com/duketemon/web-speech-recorder/tree/master/source

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='key/hopeful-hold-451623-t5-6b41c7741e03.json'


# Logging configuration
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


app = Flask(__name__)



@app.route('/')
def root():
    return app.send_static_file('index.html')

# Connection from js to server
@app.route('/mic-input', methods=['POST'])
def mic_input():
    # check if the post request has the file part
    if 'file' not in request.files:
        app.logger.error('ERROR ====> Nothing to transcribe')
        return redirect(request.url)
    
    file = request.files['file']
    language = request.form.get('language')
    micId = request.form.get('button_id')
    
    file_data = file.read()
    transcript = transcribe_audio(file_data, language)
    app.logger.info(f'INFO ====> {micId}: {transcript}')
    
    # Run translation & TTS processing in the background using threading
    # thread = threading.Thread(target=post_transcription_action, args=(micId, language, transcript))
    # thread.start()
    
    return transcript


# Get languages selection from the frontend
@app.route('/get-languages', methods=['POST'])
def get_languages():
    data = request.get_json()
    language1 = data.get("language1")
    language2 = data.get("language2")

    if not language1 or not language2:
        return jsonify({"error": "Both languages must be provided"}), 400

    app.logger.info(f"Received languages - Patient: {language1}, Health worker: {language2}")

    return jsonify({"message": "Languages received successfully", "language1": language1, "language2": language2})


# Function to transcribe audio using Google Cloud Speech-to-Text API
def transcribe_audio(file_data, language):
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=file_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code=language
    )

    response = client.recognize(config=config, audio=audio)

    # Extract the transcript from the response
    transcript = ''
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript






# # Function to run translation and TTS processing in the background
# def post_transcription_action(transcript, language, button_id,):
#     """Runs in the background to convert transcript to speech and save it locally."""
#     if not transcript.strip():
#         app.logger.info(f"No valid text received from {button_id}, skipping TTS.")
#         return
#     translate_text(transcript, language, button_id)

    


# def translate_text(text, tar_lang, button_id):
#     """Translate text to the specified target."""
#     try:
#         translator = Translator()
#         target_lang = "ml"
#         translation = translator.translate(text, dest=target_lang)
#         return translation.text
#         app.logger.info("Text to speech:{translation.text}")
#     except Exception as e:
#         app.logger.error(f"Error in translation for {button_id}: {str(e)}")
#         return None

#     return


# def generate_speech(text, output_file):
   
    
#     print(f"Audio file saved as {output_file}")
#     return

if __name__ == '__main__':
    app.run(debug=True, host='192.168.10.100', port=9045, ssl_context=('./key/cert.pem', './key/key.pem'))
    # app.run(debug=True, host='192.168.10.100', port=9045)