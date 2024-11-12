import torch
from diffusers import StableDiffusionPipeline
import pandas as pd
from openai import OpenAI
import openai
from langchain_openai import ChatOpenAI
import gradio as gr
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

openai.api_key = 'Open API key'

def generate_image_from_text(text):
    client = OpenAI()
    response = client.images.generate(
    model="dall-e-3",
    prompt=text,
    size="1024x1024",
    quality="standard",
    n=1,
    )
    image_url = response.data[0].url
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    return image

iface = gr.Interface(fn=generate_image_from_text, inputs="text", outputs="image")
iface.launch(share=True)


import openai
import gradio as gr
import os

# 設定 API 金鑰
os.environ['OPENAI_API_KEY'] = "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"
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_story(element1, element2):
    prompt = f"你是一位兒童圖書作家，請幫我生500字以内的故事情節，環境設定在熱帶雨林，並且內容包含{element1}與{element2}。"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Gradio 介面設置
iface = gr.Interface(
    fn=generate_story,
    inputs=[gr.Textbox(label="Element 1", placeholder="Type the first element here"),
            gr.Textbox(label="Element 2", placeholder="Type the second element here")],
    outputs="text"
)

iface.launch(share=True, debug=True)




