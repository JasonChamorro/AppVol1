from openai import OpenAI
import base64
import requests

secretkey = ""

prompt = ("Imagine you are the core of an app which uses user inputted images to generate ",
          "a profile for its users. Your job is to look at the provided images and create ",
          "a running list of attributes that effectively describe the user. These attributes ", 
          "should update as more images are provided. These attributes should ",
          "be specific enough that they can be used to create communities of people on ",
          "the app. Say someone uploads a photo of themselves skiing. A response like Skiier, ",
          "Outdoorsy, or Athlete would be good. Generate a list of those words and make sure they",
          "can be easily parsed and selected by code. Thank you")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

path = input("Path?\n")
paths = []

while path != "":
    paths.append(encode_image(path))
    path = input("Path?\n")


headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {secretkey}"
}

payload = {
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": str(prompt)
        },
      ]
    }
  ],
  "max_tokens": 300
}

for i in paths:
    payload["messages"][0]["content"].append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{i}"}})

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json()['choices'][0]['message']['content'])