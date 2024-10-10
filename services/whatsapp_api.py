from django.conf import settings
from requests import post, get

WHATSAPP_API_URL = 'http://134.122.115.6:3000'

if settings.DEVELOPMENT_MODE:
    WHATSAPP_API_URL = 'http://localhost:3000'

ADM_GROUP_ID = '120363334343075699@g.us'
WHATSAPP_API_SESSION = 'navegarwpp'

def get_connection_status():
    url = f'{WHATSAPP_API_URL}/session/status/{WHATSAPP_API_SESSION}/'

    try:
        response = get(url, timeout= 5)

        if response.ok:
            json = response.json()
            return json if json.get('success') else None
    except: 
        return None


def send_message(number, message):
    url = f'{WHATSAPP_API_URL}/client/sendMessage/{WHATSAPP_API_SESSION}'

    if len(number) != 10 and number != 'ADM': return None

    status = get_connection_status()

    if status:
        headers = {
            'x-api-key': f'{WHATSAPP_API_SESSION}',
        }

        chat_id = ADM_GROUP_ID if number == 'ADM' else f'55{number}@c.us'
        # chat_id = f'556899546899@c.us'
        # chat_id = ADM_GROUP_ID if number == 'ADM' else f'556899546899@c.us'

        data = {
            "chatId": chat_id,
            "contentType": "string",
            "content": message
        }

        response = post(url, json=data, timeout=5, headers=headers)

        if response.ok:
            return response.json()
    else:
        return None