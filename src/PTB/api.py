import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

base_url = f"https://api.telegram.org/bot{TOKEN}/"

method = "forwardMessages"
parameters = {
    "chat_id": "-4181556113",
    "from_chat_id": "1860278436",
    "message_ids": "[610, 611, 615]"
}

resp = requests.get(base_url + method, data=parameters)

print(resp.json())
