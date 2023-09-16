from flask import Flask, request, jsonify
import keras
import tensorflow
import numpy as np
import assemblyai as aai
import wave
import io
import requests

# replace with your API token
aai.settings.api_key = f"0831fea3924f4be890a69c8aef4b2528"
FILE_URL = "./output.wav"
api = Flask(__name__)

@api.route('/save-recording', methods=['POST'])
def save_recording():
    try:
        audio_file = request.files['audio']

        if audio_file:
            # Create a BytesIO object to work with the data
            blob_io = io.BytesIO(audio_file.read())

            # Create a WAV file
            output_wav_file = 'output.wav'  # Replace with your desired output file path

            with wave.open(output_wav_file, 'wb') as wf:
                wf.setnchannels(1)  # 1 for mono, 2 for stereo
                wf.setsampwidth(2)  # 2 bytes for 16-bit audio, adjust as needed
                wf.setframerate(91000)  # Adjust to your audio sample rate
                wf.writeframes(blob_io.read())

            # Close the BytesIO object
            blob_io.close()
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(FILE_URL)   

            return {"transcript": transcript.text}
        else:
            return 'No audio data received', 400
    except Exception as e:
        return str(e), 500


@api.route('/transcribe', methods=["POST"])
def my_profile():
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)
    return {"response": transcript.text}

@api.route('/transcribe2', methods=["GET"])
def transcribe():
    return {"response": "okey!"}

if __name__ == '__main__':
    api.run(debug=True)