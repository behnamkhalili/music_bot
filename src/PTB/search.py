import json

from thefuzz import process, fuzz

channel_list = ['Personalmusic', 'Bloop']
keys = ['file_name', 'performer', 'title']


def json_fle_reader(channels, key):
    lst = []
    for channel in channels:
        with open(f"json/{channel}.json", "r") as f:
            data = json.loads(f.read())
        for message in data['messages']:
            if "media_type" in message.keys():
                if message["media_type"] != "audio_file":
                    continue
            else:
                continue
            if key in message.keys():
                lst.append({
                    'chat_id': '-100' + str(data['id']),
                    'message_id': str(message['id']),
                    key: message[key]
                })
    return lst


def matching(lst, key, query, count):
    candidates = [music[key] for music in lst]
    fuzzied = process.extract(query, candidates, scorer=fuzz.partial_token_sort_ratio, limit=count)
    selested = [item[0] for item in fuzzied]
    selested = list(dict.fromkeys(selested))  # drop duplicates
    res = [(music, fuzz.ratio(query, music[key])) for music in lst if music[key] in selested]
    res.sort(key=sort_second, reverse=True)
    sorted_res = [tpl[0] for tpl in res]
    return sorted_res


def sort_second(val):
    return val[1]


x = json_fle_reader(channel_list, keys[1])
y = matching(x, keys[1], 'tataloo', 60)
for i in y:
    print(i, end='\n')
