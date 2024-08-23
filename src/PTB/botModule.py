import json

from thefuzz import process, fuzz

import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

url = f"https://api.telegram.org/bot{TOKEN}/"

channel_list = [
    # 'Personalmusic',
    'Bloop',
    'Ezify',
    "نه مامان بیرون یچی خوردم گشنم نیس",
    'Playlist olur gibi'
]


def json_fle_reader(channels, key):
    lst = []
    for channel in channels:
        with open(f"json/{channel}.json", "r") as f:
            data = json.loads(f.read())
        for message in data['messages']:
            if "media_type" in message.keys():
                if message["media_type"] != "audio_file" or "file_name" not in message.keys():
                    continue
            else:
                continue
            if key in message.keys():
                lst.append({
                    'chat_id': '-100' + str(data['id']),
                    'message_id': str(message['id']),
                    'file_name' : str(message['file_name']),
                    key: message[key]
                })
    return lst


def search(lst, key, query, count):
    candidates = [music[key] for music in lst]
    fuzzied = process.extract(query, candidates, scorer=fuzz.partial_token_sort_ratio, limit=count)
    selested = [item[0] for item in fuzzied]
    selested = list(dict.fromkeys(selested))  # drop duplicates
    res = [(music, fuzz.ratio(query, music[key])) for music in lst if music[key] in selested]
    res.sort(key=sort_second, reverse=True)
    sorted_res = [tpl[0] for tpl in res]
    return sorted_res[:count]


def sort_second(val):
    return val[1]


def bot_response(search_res):
    txt = "Playlist Queue:\n"
    k_music = 0
    channel_musics = {}
    for music in search_res:
        if music['chat_id'] not in channel_musics:
            channel_musics[music['chat_id']] = [int(music['message_id'])]
        else:
            channel_musics[music['chat_id']].append(int(music['message_id']))
        k_music += 1
        txt = txt + str(k_music) + ". " + music['file_name'][:-4] + "\n"
    return txt, channel_musics


def forward_musics(base_url, chat_id, musics):
    res = []
    for channel in musics:
        method = "forwardMessages"
        parameters = {
            "chat_id": chat_id,
            "from_chat_id": channel,
            "message_ids": str(sorted(musics[channel]))
        }
        resp = requests.get(base_url + method, data=parameters)
        res.append(resp.json())
    return res


def send_queue(base_url, chat_id, queue):
    method = "sendMessage"
    parameters = {
        "chat_id": chat_id,
        "text": queue
    }
    resp = requests.get(base_url + method, data=parameters)
    return resp.json()


def result(key, count, query, chat_id):
    all_musics = json_fle_reader(channel_list, key)
    matching_musics = search(all_musics, key, query, int(count))
    msg, musics = bot_response(matching_musics)
    forward_res = forward_musics(url, chat_id, musics)
    sendmsg_res = send_queue(url, chat_id, msg)
    return forward_res, sendmsg_res

