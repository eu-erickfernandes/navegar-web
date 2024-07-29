import os

from requests import post, get
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()

def session_status():
    url = f'{settings.WHATSAPP_API_URL}session/status/{settings.WHATSAPP_API_SESSION}'
    
    try:
        response = get(url)
        return response.json()
    except:
        return None


def send_message(number, message):
    url = f'{settings.WHATSAPP_API_URL}client/sendMessage/{settings.WHATSAPP_API_SESSION}'

    status = session_status()

    if status != None and status.get('success'):
        headers = {
            'x-api-key': f'{settings.WHATSAPP_API_SESSION}',
        }

        data = {
            "chatId": f"{number}@c.us",
            "contentType": "string",
            "content": message
        }

        response = post(url, json=data, timeout=10, headers=headers)

        return response.json()
    else:
        return None