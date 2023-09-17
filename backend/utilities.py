import numpy as np
import assemblyai as aai
import os
import shutil
from gradio_client import Client
from PIL import Image

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

    input_file_path = os.path.join(current_directory, input_file)
    output_directory = os.path.join(CURRENT_DIRECTORY, f'formatted{name}')

    if not extension.lower().endswith('.pdf'):
        output_pdf = png2pdf(input_file_path, output_directory)
    else:
        shutil.copy(input_file_path, f'{output_directory}.pdf')
    if name == "main":
        current_directory = os.getcwd()
        input_file = 'testPage.pdf'
        format_input(input_file)
        name, extension = os.path.splitext(input_file)

    formatted_pdf = os.path.join(CURRENT_DIRECTORY,f'formatted{name}.pdf')
    client = Client("https://ysharma-nougat.hf.space/")
    result = client.predict(
        formatted_pdf,
        "",
        fn_index=0
    )
    print(result)
    return result