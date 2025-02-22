import os
# import uuid
from flask import Flask, flash, request, redirect # type: ignore
from google.cloud import speech
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


@app.route('/save-record', methods=['POST'])
def save_record():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    language = request.form.get('language', 'en-US')
    
    file_data = file.read()
    transcript = transcribe_audio(file_data, language)
    app.logger.info(f'Transcript: {transcript}')
    return transcript


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


if __name__ == '__main__':
    app.run(debug=True, host='192.168.10.100', port=9045, ssl_context=('./key/cert.pem', './key/key.pem'))
    # app.run(debug=True, host='192.168.10.100', port=9045)