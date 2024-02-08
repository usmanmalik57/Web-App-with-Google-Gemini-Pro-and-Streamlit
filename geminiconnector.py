import os
from vertexai.preview.generative_models import GenerativeModel, Part
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"your_api_file.json"

model = GenerativeModel("gemini-pro-vision")
config={
    "max_output_tokens": 2048,
    "temperature": 0,
    "top_p": 1,
    "top_k": 32
}


def generate(img, prompt):

    input = img + [prompt]

    responses = model.generate_content(    
        input,
        generation_config= config,
        stream=True,
    )
    full_response = ""

    for response in responses:
        full_response += response.text

    return full_response

  