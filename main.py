from geminiconnector import generate
from vertexai.preview.generative_models import Part
import streamlit as st
import pandas as pd
import os
import base64
import glob
import re
import csv


st.write("# Image Table Extractor")
uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=['jpg', 'png'])


def save_uploaded_files(directory, uploaded_files):

    if not os.path.exists(directory):
        os.makedirs(directory)  

    for uploaded_file in uploaded_files:
        file_path = os.path.join(directory, uploaded_file.name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

local_dir = "tempdir"

if st.button('Upload Images'):
    if uploaded_files:

        save_uploaded_files(local_dir, uploaded_files)
        st.success(f'Images have been Uploaded.')

    else:
        st.error('Please upload at least one image.')


def get_jpg_file_paths(directory):

    jpg_file_paths = glob.glob(os.path.join(directory, '**', '*.jpg'), recursive=True)
    return [os.path.abspath(path) for path in jpg_file_paths]


def read_image(img_paths):

    imgs_b64 = []
    for img in img_paths:
        with open(img, "rb") as f: # open the image file in binary mode
            img_data = f.read() # read the image data as bytes
            img_b64 = base64.b64encode(img_data) # encode the bytes as base64
            img_b64 = img_b64.decode() # convert the base64 bytes to a string
            img_b64 = Part.from_data(data=img_b64, mime_type="image/jpeg")

            imgs_b64.append(img_b64)

    return imgs_b64




def process_line(line):

    lines = full_response.strip().split('\n')

    special_patterns = re.compile(r'\d+,\d+\s[€%]')

    temp_replacement = "TEMP_CURRENCY"

    currency_matches = special_patterns.findall(line)

    for match in currency_matches:
        line = line.replace(match, temp_replacement, 1)

    parts = line.split(',')

    for i, part in enumerate(parts):
        if temp_replacement in part:
            parts[i] = currency_matches.pop(0)

    return parts

st.write("## Enter your query.")
user_input = st.text_area("query", 
                          height=100,
                          label_visibility = "hidden")

if st.button('Submit Query'):

    image_paths = get_jpg_file_paths(local_dir)
    imgs_b64 = read_image(image_paths)
    full_response = generate(imgs_b64, user_input)

    lines = full_response.strip().split('\n')

    data = []

    for line in lines:
        processed_line = process_line(line) 
        data.append(processed_line)
 
    df = pd.DataFrame(data)

    st.write("### Output")

    st.write(df)

    