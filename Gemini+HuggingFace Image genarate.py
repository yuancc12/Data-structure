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

api_base_url = "https://web-tech-tw.eu.org/openai/v1"
api_key = "AIzaSyCR5l1ZDJ-lMp7uvgQhIE44HNcn36kvRKE"
def generate_image_from_text(text):
    combined_text = text+"，英文翻譯給我"
    client = OpenAI()
    response = client.images.generate(
    model="dall-e-3",
    prompt=text,
    size="1024x1024",
    quality="standard",
    n=1,
    )
    image_url = response.data[0].url
    completion = client.chat.completions.create(model="gpt-3.5-turbo",messages=[{"role": "system", "content": "你好，我是繪畫家"},{"role": "user", "content": combined_text}],)
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    return image


# Load the model to CPU instead of CUDA
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float32)
pipe.to(device)

iface = gr.Interface(fn=generate_image_from_text, inputs="text", outputs="image")
iface.launch(share=True)




