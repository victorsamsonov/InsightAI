import requests
import config
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
import io
from pydub import AudioSegment
import json

APP_KEY = "3c9a7ad798ebeb8d5c6b74d30b902c38aa1c56cd1cc4d78f10cdc4ae4bbd88aa"
APP_ID = "insightai_c0fe0f_bf33f1"

def identify_learning_style_and_hobby(transcript):
    """
    Identify the learning style and hobby from the given transcript.
    Uses OpenAI API to extract this information based on the content of the transcript.
    """
    ENDPOINT = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.OPENAI_API_KEY}",
    }

    def make_api_call(messages):
        data = {
            "model": "gpt-4",   # Specify the model, adjust if necessary
            "messages": messages
        }
        response = requests.post(ENDPOINT, headers=headers, json=data)
        response_data = response.json()
        
        # Log the full API response for debugging
        print(response_data)

        if 'choices' in response_data:
            return response_data['choices'][0]['message']['content'].strip()
        else:
            print(f"Unexpected API response for messages: {messages}")
            return "Error extracting data"
    
    # Extract hobbies or experiences for analogies
    messages_experience = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"The person mentioned: '{transcript}'. Extract a hobby or personal experience they might have talked about and write one sentence of that so that we can use that for creating analogies in the future."}
    ]
    experience_summary = make_api_call(messages_experience)

    # Extract preferred explanation style
    messages_style = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"The person mentioned: '{transcript}'. Identify their preferred explanation style and return in one concise sentence."}
    ]
    style_summary = make_api_call(messages_style)

    return style_summary, experience_summary

def convert_audio_to_required_format(audio_file_path, target_format='wav'):
    """
    Convert audio file to the format required by Google Speech-to-Text.
    The target format is LINEAR16 with a sample rate of 16000 Hz.
    """
    audio = AudioSegment.from_file(audio_file_path, format="auto")
    audio = audio.set_frame_rate(16000)
    audio = audio.set_channels(1)  # mono channel
    temp_path = "temp_converted_audio.wav"
    audio.export(temp_path, format=target_format, codec='pcm_s16le')  # LINEAR16
    return temp_path

def speech_to_text(audio_file_path):
    """
    Convert the provided audio file to text using Google's Speech-to-Text API.
    """
    
    # Convert the audio to the required format
    converted_audio_path = convert_audio_to_required_format(audio_file_path)

    client = speech.SpeechClient()

    with io.open(converted_audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Use long_running_recognize for longer audio files
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=360)  # Adjust timeout as needed

    transcribed_text = ""
    for result in response.results:
        transcribed_text += result.alternatives[0].transcript + " "

    return transcribed_text.strip()

#for mathpix
def extract_image_content(image_path):
    """
    Extract content from an image using the Mathpix API.
    This function currently extracts formatted content in the form of LaTeX, 
    but can be adjusted as per the API's capabilities.
    """

    r = requests.post("https://api.mathpix.com/v3/text",
    files={"file": open(image_path,"rb")},
    data={
      "options_json": json.dumps({
        "math_inline_delimiters": ["$", "$"],
        "rm_spaces": True
      })
    },
    headers={
        "app_id": APP_ID,
        "app_key": APP_KEY
    }
)
    return json.dumps(r.json(), indent=4, sort_keys=True)


def get_gpt_response(user_query, image_content, user_style, user_hobby):
    ENDPOINT = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.OPENAI_API_KEY}",
    }
    
    prompt = f"Given that the user said '{user_query}' and referred to the content '{image_content}', and they prefer explanations in a '{user_style}' learning style using analogies related to '{user_hobby}', explain the concept to them."

    messages = [
        {"role": "system", "content": "You are a helpful personal tutor that can understand the the image context that is either returned in latex or SMILES and use your understanding of that to answer the users query/confusion according to their learning style and analogies using their hobbies"},
        {"role": "user", "content": prompt}
    ]

    response = requests.post(ENDPOINT, headers=headers, json={"model": "gpt-4", "messages": messages})
    response_data = response.json()

    if 'choices' in response_data:
        return response_data['choices'][0]['message']['content'].strip()
    else:
        print(f"Unexpected API response for messages: {messages}")
        return "I'm sorry, I couldn't generate a response at the moment."


def text_to_voice(text):
    """
    Convert the given text to voice using Google's Text-to-Speech API.
    The function currently outputs an MP3 file.
    """
    
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    output_audio_path = "output_voice_response.mp3"
    with open(output_audio_path, 'wb') as out:
        out.write(response.audio_content)

    return output_audio_path