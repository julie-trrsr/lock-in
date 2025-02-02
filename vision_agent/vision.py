from IPython.display import display, Image, Audio

import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
import time
from openai import OpenAI
import os
import requests
import asyncio
from dotenv import load_dotenv
from anthropic import Anthropic
import json
from abc import ABC, abstractmethod

# Load environment variables from secrets.env
load_dotenv("../secrets.env")

# Retrieve the API key
# openai_api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=openai_api_key)
claude_api_key = os.getenv("CLAUDE_API_KEY")
video = cv2.VideoCapture("data/bird.mp4")

base64Frames = []

while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpeg", frame)
    if(len(base64Frames) <1):
        base64Frames.append(base64.standard_b64encode(buffer).decode("utf-8"))
    # single_image = base64.standard_b64encode(buffer).decode("utf-8")

video.release()
print(len(base64Frames), "frames read.")

# import base64
import httpx

# image1_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
# image1_media_type = "image/jpeg"
# image1_data = base64.standard_b64encode(httpx.get(image1_url).content).decode("utf-8")

# image2_url = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg"
# image2_media_type = "image/jpeg"
# image2_data = base64.standard_b64encode(httpx.get(image2_url).content).decode("utf-8")

# client = anthropic.Client(claude_api_key)
def shoping_list(item):
    return (len(item)*100)


tool_definition = {
    "name": "animal_price_calculator",
    "description": "animal price calculator",
    "input_schema": {
        "type": "object",
        "properties": {
            "item": {
                "type": "string",
                "description": "calculate item price"
            }
        },
        "required": ["item"]
    }
}



content = [{"type": "text", "text": "These two images are the point of view of the user. These two image shows the before and after of the user distracted by something. Please identify what is the distraction is present and list the objects that distracted the user."}]  # Start with the prompt

# Add each image to the content array
# for base64_frame in base64Frames:  # Limit to first 10 frames
#     image_content = {
#         "type": "image",
#         "source": {
#             "type": "base64",
#             "media_type": "image/jpeg",
#             "data": base64_frame
#         }
#     }
#     content.append(image_content)


image_content = {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": base64.standard_b64encode(open('data/working.jpeg', 'rb').read()).decode("utf-8")
        }
    }

content.append(image_content)

image_content = {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": base64.standard_b64encode(open('data/not_working.jpeg', 'rb').read()).decode("utf-8")
        }
    }

content.append(image_content)


client = Anthropic(api_key=claude_api_key)
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system= "You are a Visual Context Agent. Your role is to analyze images and identify key elements relevant to distraction detection:",
    messages=[
        {
            "role": "user",
            "content": content
        }
    ],
    tools=[tool_definition],
)
print(message)


import role
target_model = "claude-3-5-sonnet-20241022"


class base_agent(ABC):
    def __init__(self, system_role, system_query):
        self.client = Anthropic(api_key=claude_api_key)
        self.system_role = system_role
        self.system_query = system_query
    
    async def process_with_claude(self, input_images):
        try:
            combined_message = [{"role": "user", "type": "text", "text":self.system_query}]   
            for input_image in input_images:
                combined_message.append(input_image)
            
            response = await self.client.messages.create(
                model=target_model,
                system=self.system_role,
                message= combined_message,
                max_tokens=2048,
            )
            return json.loads(response.content)
        except Exception as e:
            print(f"Error calling Claude API: {str(e)}")
            raise


class ObjectClassifierAgent(base_agent):
    def __init__(self):
        system_prompt = role.object_classifier_agent
        system_query = role.object_classifier_query
        super().__init__(system_prompt, system_query)
        
    async def process(self, image_data):
        return await self.process_with_claude(image_data)
    
class ObjectClassifierAgent(base_agent):
    def __init__(self):
        system_prompt = role.object_classifier_agent
        system_query = role.object_classifier_query
        super().__init__(system_prompt, system_query)
        
    async def process(self, image_data):
        return await self.process_with_claude(image_data)



