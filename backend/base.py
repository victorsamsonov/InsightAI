from PIL import Image
import requests
from transformers import AutoProcessor, BlipModel
import requests
import json
from utils import identify_learning_style_and_hobby, speech_to_text, get_gpt_response, text_to_voice, extract_image_content
import os
import base64
import config

APP_KEY = "3c9a7ad798ebeb8d5c6b74d30b902c38aa1c56cd1cc4d78f10cdc4ae4bbd88aa"
APP_ID = "insightai_c0fe0f_bf33f1"

# r = requests.post("https://api.mathpix.com/v3/text",
#     files={"file": open("curr.png","rb")},
#     data={
#       "options_json": json.dumps({
#         "math_inline_delimiters": ["$", "$"],
#         "rm_spaces": True
#       })
#     },
#     headers={
#         "app_id": APP_ID,
#         "app_key": APP_KEY
#     }
# )
# print(json.dumps(r.json(), indent=4, sort_keys=True))
USER_STYLE = "receive detailed step by step explanations, understanding intuition behind concepts is essential."
USER_HOBBY = "Listening to music and basketball"
from flask import Flask, request, jsonify
import numpy as np
import assemblyai as aai
import wave
import os
import io
from gradio_client import Client
from PIL import Image
import replicate
# from utilities import png2pdf, format_input
# replace with your API token
aai.settings.api_key = f"0831fea3924f4be890a69c8aef4b2528"
FILE_URL = "./output.wav"
CURRENT_DIRECTORY = "./"
api = Flask(__name__)
replicate.Client(api_token="r8_WCrcrURA2cbG8qRKhY8Ey79dNiP1pUv16Dwer")
import numpy as np
import assemblyai as aai
import os
import shutil
from gradio_client import Client
from PIL import Image

# if __name__ == "__main__":
#         current_directory = CURRENT_DIRECTORY
#         # current_directory = os.path.join(current_directory, 'backend')
#         input_file = 'curr.png'
#         name, extension = os.path.splitext(input_file)

#         # input_file_path = os.path.join(current_directory, input_file)
#         output_path = "./curr" + ".pdf"

#         if not extension.lower().endswith('.pdf'):
#             image_1 = Image.open(f'{"./curr.png"}')
#             im_1 = image_1.convert('RGB')
#             im_1.save(output_path)

#         client = Client("https://ysharma-nougat.hf.space/")
#         print(client)
#         result = client.predict(
#             output_path,
#             "",
#             fn_index=0
#         )
#         response = result
#         print(output_path)
#         print(result)

CURRENT_DIRECTORY = "./"

def png2pdf(png, output_path):
    """
    returns pdf file path
    """
    image_1 = Image.open(f'{png}')
    im_1 = image_1.convert('RGB')
    im_1.save(f'{output_path}.pdf')


def format_input(input_file):
    current_directory = os.getcwd()
    name, extension = os.path.splitext(input_file)

    input_file_path = os.path.join(CURRENT_DIRECTORY, name )
    output_directory = os.path.join(CURRENT_DIRECTORY, f'{name}')

    if not extension.lower().endswith('.pdf'):
        output_pdf = png2pdf(input_file, output_directory)
    else:
        shutil.copy(input_file_path, f'{output_directory}.pdf')
    
    # if __name__ == "__main__":
    #     current_directory = os.getcwd()
    #     # input_file = 'fullHalf.pdf'
    #     format_input(input_file)
    #     name, extension = os.path.splitext(input_file)
        
    # pdf2math(formatted_pdf, f'{current_directory}/{name}.txt')
    output = replicate.run(
    "andreasjansson/blip-2:4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608",
    input={"image": open("path/to/file", "rb")}
    )
    print(output)
    formatted_pdf = os.path.join(CURRENT_DIRECTORY,f'{name}.pdf')
    from gradio_client import Client

    client = Client("https://ysharma-nougat.hf.space/")
    result = client.predict(
        formatted_pdf,
        "",
        fn_index=0
    )
    print(result)
    return result


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


@api.route('/predict', methods=["POST"])
def predict():
    print(request.files)
    image_file = request.files["file"]
    if image_file:
        image_file.save("./curr.png")
    response = None
    r = requests.post("https://api.mathpix.com/v3/text",
    files={"file": open("curr.png","rb")},
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
    print(json.dumps(r.json(), indent=4, sort_keys=True))

    return json.dumps(r.json(), indent=4, sort_keys=True)
#     return {"text": """"5.4 Repetitions during inference
# We notice that the model degenerates into repeating the same sentence over and over again. The model can not recover from this state by itself. In its simplest form, the last sentence or paragraph is repeated over and over again. We observed this behavior in $1.5 \%$ of pages in the test set, but the frequency increases for out-of-domain documents. Getting stuck in a repetitive loop is a known problem with Transformer-based models, when sampled with greedy decoding [44]. It can also happen that the model alternates between two sentences but sometimes changes some words, so a strict repetition detection will not suffice. Even harder to detect are predictions where the model counts its own repetitions, which sometimes happens in the references section.
# In general we notice this kind behavior after a mistake by the model. The model is not able to recover from the collapse.
# Anti-repetition augmentation Because of that we introduce a random perturbation during training. This helps the model to learn how to handle a wrongly predicted token. For each training example, there is a fixed probability that a random token will be replaced by any other randomly chosen token. This process continues until the newly sampled number is greater than a specified threshold (in this case, $10 \%$ ). We did not observe a decrease in performance with this approach, but we did notice a significant reduction in repetitions. Particularly for out-of-domain documents, where we saw a $32 \%$ decline in failed page conversions.

# Repetition detection Since we are generating a maximum of 4096 tokens the model will stop at some point, however it is very inefficient and resource intensive to wait for a "end of sentence" token, when none will come. To detect the repetition during inference time we look at the largest logit value $\ell_{i}=\max \ell_{i}$ of the ith token. We found that the logits after a collapse can be separated using the following heuristic. First calculate the variance of the logits for a sliding window of size $B=15$
# \[
# \operatorname{VarWin}_{B}[\ell](x)=\frac{1}{B} \sum_{i=x}^{x+B}\left(\ell_{i}-\frac{1}{B} \sum_{j=x}^{x+B} \ell_{j}\right)^{2} .
# \]
# 8"""}

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_CREDENTIALS_PATH

# A dictionary to store user information, e.g., learning style and hobby
USERS = {}

@api.route('/onboarding', methods=['POST'])
def onboarding():
    """
    This route handles the onboarding process for a user. 
    It expects an audio file where the user talks about their preferences.
    The function saves the audio file, converts it to text, and then extracts 
    the learning style and any hobby or personal experience mentioned by the user.
    The results are stored in a USERS dictionary for future use.
    After processing, all temporary files are deleted.
    """

    audio_file = request.files.get('audio_file')
    audio_file.save("audio.wav")  # Save the audio file temporarily

    # Convert the audio file to text
    transcript = speech_to_text("audio.wav")

    # Extract the user's learning style and any mentioned hobby/experience
    style_summary, experience_summary = identify_learning_style_and_hobby(transcript)

    # Store the extracted data for the user
    USERS['default_user'] = {'style': style_summary, 'hobby': experience_summary}

    # Cleanup: remove temporary files
    os.remove("audio.wav")

    # Check if the converted audio file exists before removing it
    if os.path.exists("temp_converted_audio.wav"):
        os.remove("temp_converted_audio.wav")

    # Return a success message along with the extracted data
    return jsonify({"message": "Onboarding successful", 
                    "style": style_summary, 
                    "experience": experience_summary}), 200


@api.route('/process-image', methods=['POST'])
def process_image():
    """
    Process an uploaded image and extract its content.
    Currently uses Mathpix for image content extraction.
    """

    # Retrieve the uploaded image from the request
    image_file = request.files.get('image_file')
    image_path = "curr.png"
    image_file.save(image_path)  # Save the uploaded image temporarily

    # Extract content from the image using Mathpix API
    image_content = extract_image_content(image_path)

    # Cleanup: remove the saved image after processing
    os.remove(image_path)

    # Return a success message and the extracted content
    return jsonify({"message": "Image processed successfully", "content": image_content}), 200

@api.route('/generate-response', methods=['POST'])
def generate_response():
    """
    Generate a response based on the uploaded image's content and user preferences.
    The function uses the content from the image and previously stored user data 
    (from the onboarding process) to generate a GPT response. The text response 
    is then converted to an audio format.
    """
    # Retrieve the uploaded image and audio query from the request
    # image_file = request.files.get('image_file')
    audio_query_file = request.json.get('audio_query')
    
    # Save the uploaded image temporarily
    image_path = "curr.png"
    # image_file.save(image_path)  

    # Save the audio query temporarily
    # audio_query_path = "audio_query.wav"
    # audio_query_file.save(audio_query_path)

    # Convert the audio query to text
    user_query = audio_query_file

    # Extract content from the image using Mathpix API
    image_content = extract_image_content(image_path)

    # Get user data stored during the onboarding process
    user_data = USERS.get('default_user', {})
    user_style = user_data.get('style', '')
    user_hobby = user_data.get('hobby', '')

    # Generate a GPT-4 response based on the image content, user query, and user data
    gpt_response = get_gpt_response(user_query, image_content, USER_STYLE, USER_HOBBY)

    # Convert the text response to audio
    voice_response_path = text_to_voice(gpt_response)
    
    # Convert the .wav file to base64 before sending
    with open(voice_response_path, 'rb') as file:
        wav_data = base64.b64encode(file.read()).decode('utf-8')

    # Cleanup: remove the saved files after processing
    os.remove(image_path)
    # os.remove(audio_query_path)

    # Return a success message and the path to the generated audio response
    return jsonify({"message": "Response generated successfully", "audio_path": wav_data}), 200


if __name__ == '__main__':
    api.run(debug=True)