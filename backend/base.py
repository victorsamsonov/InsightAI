from PIL import Image
import requests
from transformers import AutoProcessor, BlipModel

model = BlipModel.from_pretrained("Salesforce/blip-image-captioning-base")
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")

url = "curr.png"
image = Image.open(url)

# inputs = processor(
#     text=["a photo of a cat", "a photo of a dog"], images=image, return_tensors="pt", padding=True
# )

inputs = processor(images=image, text="A picture of", return_tensors="pt")

outputs = model(**inputs)
print(outputs)
# from flask import Flask, request, jsonify
# import numpy as np
# import assemblyai as aai
# import wave
# import os
# import io
# from gradio_client import Client
# from PIL import Image
# import replicate
# # from utilities import png2pdf, format_input
# # replace with your API token
# aai.settings.api_key = f"0831fea3924f4be890a69c8aef4b2528"
# FILE_URL = "./output.wav"
# CURRENT_DIRECTORY = "./"
# api = Flask(__name__)
# replicate.Client(api_token="r8_WCrcrURA2cbG8qRKhY8Ey79dNiP1pUv16Dwer")
# import numpy as np
# import assemblyai as aai
# import os
# import shutil
# from gradio_client import Client
# from PIL import Image

# # if __name__ == "__main__":
# #         current_directory = CURRENT_DIRECTORY
# #         # current_directory = os.path.join(current_directory, 'backend')
# #         input_file = 'curr.png'
# #         name, extension = os.path.splitext(input_file)

# #         # input_file_path = os.path.join(current_directory, input_file)
# #         output_path = "./curr" + ".pdf"

# #         if not extension.lower().endswith('.pdf'):
# #             image_1 = Image.open(f'{"./curr.png"}')
# #             im_1 = image_1.convert('RGB')
# #             im_1.save(output_path)

# #         client = Client("https://ysharma-nougat.hf.space/")
# #         print(client)
# #         result = client.predict(
# #             output_path,
# #             "",
# #             fn_index=0
# #         )
# #         response = result
# #         print(output_path)
# #         print(result)

# CURRENT_DIRECTORY = "./"

# def png2pdf(png, output_path):
#     """
#     returns pdf file path
#     """
#     image_1 = Image.open(f'{png}')
#     im_1 = image_1.convert('RGB')
#     im_1.save(f'{output_path}.pdf')


# def format_input(input_file):
#     current_directory = os.getcwd()
#     name, extension = os.path.splitext(input_file)

#     input_file_path = os.path.join(CURRENT_DIRECTORY, name )
#     output_directory = os.path.join(CURRENT_DIRECTORY, f'{name}')

#     if not extension.lower().endswith('.pdf'):
#         output_pdf = png2pdf(input_file, output_directory)
#     else:
#         shutil.copy(input_file_path, f'{output_directory}.pdf')
    
#     # if __name__ == "__main__":
#     #     current_directory = os.getcwd()
#     #     # input_file = 'fullHalf.pdf'
#     #     format_input(input_file)
#     #     name, extension = os.path.splitext(input_file)
        
#     # pdf2math(formatted_pdf, f'{current_directory}/{name}.txt')
#     output = replicate.run(
#     "andreasjansson/blip-2:4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608",
#     input={"image": open("path/to/file", "rb")}
#     )
#     print(output)
#     formatted_pdf = os.path.join(CURRENT_DIRECTORY,f'{name}.pdf')
#     from gradio_client import Client

#     client = Client("https://ysharma-nougat.hf.space/")
#     result = client.predict(
#         formatted_pdf,
#         "",
#         fn_index=0
#     )
#     print(result)
#     return result


# @api.route('/save-recording', methods=['POST'])
# def save_recording():
#     try:
#         audio_file = request.files['audio']
#         if audio_file:
#             # Create a BytesIO object to work with the data
#             blob_io = io.BytesIO(audio_file.read())

#             # Create a WAV file
#             output_wav_file = 'output.wav'  # Replace with your desired output file path

#             with wave.open(output_wav_file, 'wb') as wf:
#                 wf.setnchannels(1)  # 1 for mono, 2 for stereo
#                 wf.setsampwidth(2)  # 2 bytes for 16-bit audio, adjust as needed
#                 wf.setframerate(91000)  # Adjust to your audio sample rate
#                 wf.writeframes(blob_io.read())

#             # Close the BytesIO object
#             blob_io.close()
#             transcriber = aai.Transcriber()
#             transcript = transcriber.transcribe(FILE_URL)   

#             return {"transcript": transcript.text}
#         else:
#             return 'No audio data received', 400
#     except Exception as e:
#         return str(e), 500


# @api.route('/transcribe', methods=["POST"])
# def my_profile():
#     transcriber = aai.Transcriber()
#     transcript = transcriber.transcribe(FILE_URL)
#     return {"response": transcript.text}


# @api.route('/predict', methods=["POST"])
# def predict():
#     print(request.files)
#     audio_file = request.files['audio']
#     image_file = request.files["file"]
#     if audio_file:
#             # Create a BytesIO object to work with the data
#             blob_io = io.BytesIO(audio_file.read())
#             # Create a WAV file
#             output_wav_file = 'output.wav'  # Replace with your desired output file path
#             with wave.open(output_wav_file, 'wb') as wf:
#                 wf.setnchannels(1)  # 1 for mono, 2 for stereo
#                 wf.setsampwidth(2)  # 2 bytes for 16-bit audio, adjust as needed
#                 wf.setframerate(91000)  # Adjust to your audio sample rate
#                 wf.writeframes(blob_io.read())
#     if image_file:
#         image_file.save("./curr.png")
#     response = None
#     # if __name__ == "__main__":
#     #     current_directory = os.getcwd()
#     #     input_file = 'curr.png'
#     #     name, extension = os.path.splitext(input_file)

#     #     input_file_path = os.path.join(current_directory, input_file)
#     #     output_path = os.path.splitext(input_file_path)[0] + ".pdf"

#     #     if not extension.lower().endswith('.pdf'):
#     #         image_1 = Image.open(f'{input_file_path}')
#     #         im_1 = image_1.convert('RGB')
#     #         im_1.save(output_path)

#     #     from gradio_client import Client

#     #     client = Client("https://ysharma-nougat.hf.space/")
#     #     result = client.predict(
#     #         "./curr.pdf",
#     #         "",
#     #         fn_index=0
#     #     )
#     #     response = result
#     #     print(output_path)

    
#     # client = Client("https://fffiloni-clip-interrogator-2.hf.space/")
#     # result = client.predict(
#     #                 "curr.png",    # str (filepath or URL to image) in 'parameter_3' Image component
#     #                 "best",    # str in 'Select mode' Radio component
#     #                 2,    # int | float (numeric value between 2 and 24) in 'best mode max flavors' Slider component
#     #                 api_name="/clipi2"
#     # )
#     output = replicate.run(
#     "andreasjansson/blip-2:4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608",
#     input={"image": open("./curr.png", "rb")}
#     )
#     # response = format_input("./curr.png")
#     return {"response": output}

# if __name__ == '__main__':
#     api.run(debug=True)