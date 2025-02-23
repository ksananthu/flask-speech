import os
import threading
import asyncio
from gtts import gTTS # type: ignore
from flask import Flask, request, redirect, jsonify,  Response # type: ignore
from google.cloud import speech
from googletrans import Translator # type: ignore
from dotenv import load_dotenv
import logging

load_dotenv()

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


# Logging configuration
logging.basicConfig(filename='log/app.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


app = Flask(__name__)

# Global variables to store languages
patientLan = None
workerLan = None



@app.route('/')
def root():
    delete_all_audio_files()
    return app.send_static_file('index.html')


@app.route('/mic-input', methods=['POST'])
def mic_input():
    """
    Receive audio file from the frontend and create a transcription
    
    Returns:
        transcript : Transcription of the audio file
    """
    # check if the post request has the file part
    if 'file' not in request.files:
        app.logger.error('ERROR ====> Nothing to transcribe')
        return jsonify({"error": "⚠️ No speech detected. Please try again."}), 400
    
    file = request.files['file']
    src_language = request.form.get('language')
    micId = request.form.get('button_id')
    
    file_data = file.read()
    # if file_data 
    transcript = transcribe_audio(file_data, src_language)

    if transcript:
        app.logger.info(f'INFO ====> {micId}: {transcript}')
        #Run translation & TTS processing in the background using threading
        thread = threading.Thread(target=post_transcription_action, args=(transcript, src_language, micId))
        thread.start()
        
        return transcript
    else:
        delete_file_or_directory(micId)
        app.logger.error("⚠️ No speech detected or Change change language and try again.")
        return jsonify({"error": "⚠️ No speech detected or Language is not recognized ."}), 400
    
    


@app.route('/play-audio', methods=['POST'])
def play_audio():
    """
    Play audio file on the frontend on click of the play button
    
    """
    data = request.get_json()
    button_id = data.get('button_id')

    if button_id == "playTTSButton":
        file_path = './audio/patient.mp3'
    elif button_id == "playTTSButton2":
        file_path = './audio/healthworker.mp3'
    else:
        return jsonify({"error": "Invalid button ID"}), 400

    if os.path.exists(file_path):
        # Define generate() inside this block
        def generate():
            with open(file_path, "rb") as audio_file:
                yield from audio_file  # Stream the audio file in chunks

        return Response(generate(), mimetype="audio/mp3")
    else:
        app.logger.error("Audio file not found")
        return jsonify({"error": "Audio file not found"}), 404
        




# Get languages selection from the frontend
@app.route('/get-languages', methods=['POST'])
def get_languages():
    """
    Get languages selected by the patient and health worker
    """
    
    # Access global variables
    global patientLan, workerLan
    
    data = request.get_json()
    patientLan = data.get("patientLan")
    workerLan = data.get("workerLan")

    if not patientLan or not workerLan:
        return jsonify({"error": "Both languages must be provided"}), 400

    app.logger.info(f"Received languages : Patient: {patientLan}, Health worker: {workerLan}")

    return jsonify({"message": "Languages received successfully", "patientLan": patientLan, "workerLan": workerLan})



def delete_all_audio_files():
    """
    Deletes all audio files inside the 'audio/' directory.
    """
    audio_dir = './audio/'

    if not os.path.exists(audio_dir):
        app.logger.info("Audio directory does not exist.")
        return

    try:
        for file in os.listdir(audio_dir):
            file_path = os.path.join(audio_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                app.logger.info(f"Deleted: {file_path}")
    except Exception as e:
        app.logger.error(f"Error deleting audio files: {e}")


# Function to transcribe audio using Google Cloud Speech-to-Text API
def transcribe_audio(file_data, src_language):
    """Get transcription of the audio file using Google Cloud Speech-to-Text API.

    Args:
        file_data (_audio_): Audio file data to be transcribed
        src_language (str): Source language of the audio file

    Returns:
        text: Description of the audio file
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=file_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code=src_language
    )

    response = client.recognize(config=config, audio=audio)

    # Extract the transcript from the response
    transcript = ''
    for result in response.results:
        transcript += result.alternatives[0].transcript
        

    return transcript




# Function to run translation and TTS processing in the background
def post_transcription_action(transcript, src_language, micId):
    """Get translation of the audio file and convert it to speech. Run in the background.

    Args:
        transcript (text): Transcription of the audio file
        src_language (text): source language of the audio file
        micId (text): Represents who is speaking (patient or health worker)
    """
    
    delete_file_or_directory(micId) # Delete previous audio file
    if not transcript:
        app.logger.info(f"No valid text received from : {micId}, skipping Speech to text.")
        return
    
    global patientLan, workerLan
    
    if micId == "recordButton": # recordButton is for patient & replayButton2 is for health worker
        tar_language = workerLan
        identity = "patient"
    else:
        tar_language = patientLan
        identity = "healthworker"
    
    tar_language = str(tar_language)[:2]
    filename = f"./audio/{identity}.mp3"
    
    translated_txt = translate_text(transcript, src_language, tar_language)
    
    text_to_speech(translated_txt, filename, tar_language)

    


def translate_text(text, src_lang, tar_lang):
    
    """Translate text from source language to target language.

    Returns:
        text: text translated to the target language
    """
    
    try:
        translator = Translator()
        tar_lang = str(tar_lang)[:2]
        src_lang = str(src_lang)[:2]
        
        app.logger.info(f"Text : {text}")
        app.logger.info(f"Destination Language : {src_lang}")
        app.logger.info(f"Source Language : {tar_lang} ")
        
        if tar_lang == src_lang:
            app.logger.info(f"Text to speech:{text}")
            return text
        else:
            translation = asyncio.run(translator.translate(text, dest=tar_lang, src=src_lang))
            app.logger.info(f"Text to speech: {translation.text}")
            return translation.text
    except Exception as e:
        app.logger.error(f"Error in translation for: {str(e)}")
        return None


def delete_file_or_directory(micId):
    """
    Deletes previous audio file of patients / workers.

    Args:
        micId: micId to identify who is speaking.

    Returns:
        True if the file/directory was successfully deleted, False otherwise.
        Prints informative messages to the console in case of errors.
    """
    
    if micId == "recordButton": # recordButton is for patient & replayButton2 is for health worker
        path = './audio/patient.mp3'
    else:
        path = './audio/healthworker.mp3'
    
    try:
        if os.path.isfile(path):  # Check if it's a file
            os.remove(path)
            app.logger.info(f"File '{path}' deleted successfully.")
        return True
        
    except FileNotFoundError:
        return False
    except OSError as e:  # Catch more specific OS errors (permissions, etc.)
        app.logger.error(f"Error deleting '{path}': {e}")
        return False
    except Exception as e: # Catch any other exceptions
        app.logger.error(f"An unexpected error occurred: {e}")
        return False


def text_to_speech(text, filename, lang):
    """
    Converts text to speech and saves it as an MP3 file.

    Args:
        text: The text to be converted to speech.
        filename: The name of the output MP3 file (default: "output.mp3").
        lang: The language code for the speech (default: "en" for English).  See gTTS documentation for other language codes.

    Returns:
       True if the speech file was created successfully, False otherwise.  Prints error messages to the console.
    """
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        app.logger.info(f"Speech file '{filename}' created successfully.")
        return True
    except ValueError as e:
      app.logger.error(f"Error: {e}") # Likely an unsupported language code
      return False
    except Exception as e:  # Catch a wider range of potential errors
        app.logger.error(f"An unexpected error occurred: {e}")
        return False



if __name__ == '__main__':
    app.run(debug=True, host='192.168.10.100', port=9045, ssl_context=('./key/cert.pem', './key/key.pem'))
    # app.run(debug=True, host='192.168.10.100', port=9045)