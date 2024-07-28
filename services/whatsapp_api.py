import os

from requests import post, get
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()

host = os.getenv('HOST_IP', 'HOST_IP')
port = os.getenv('PORT', 'PORT')
session = os.getenv('SESSION_NAME', 'SESSION_NAME')

def session_status():
    url = f'http://{host}:{port}/session/status/{session}'

    response = get(url)

    return response.json()

def send_message(number, message):
        url = f'http://{host}:{port}/client/sendMessage/{session}'

        headers = {
            'x-api-key': session,
        }

        data = {
            "chatId": f"{number}@c.us",
            "contentType": "string",
            "content": message
        }

        response = post(url, json=data, timeout=10, headers=headers)
        return response.json()