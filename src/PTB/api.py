import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

base_url = f"https://api.telegram.org/bot{TOKEN}/"

method = "forwardMessages"
parameters = {
    "chat_id": "-4181556113",
    "from_chat_id": "-1001234468921",
    "message_ids": "[1158, 1159, 2000]"
}

resp = requests.get(base_url + method, data=parameters)

print(resp.json())
