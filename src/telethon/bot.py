from telethon import TelegramClient

from dotenv import load_dotenv
import os

import logging

load_dotenv()
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('anon', api_id, api_hash)

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


async def main():
    me = await client.get_me()
    print(me.stringify())

    username = me.username
    print(username)
    print(me.phone)

    # You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

    await client.send_message('me', 'Hello, myself!')
    await client.send_message('Sad bHnM', 'Hello, friend!')
    await client.send_message(-1002173884915, 'Testing Telethon!')

    message = await client.send_message(
        'me',
        'This message has **bold**, `code`, __italics__ and '
        'a [nice website](https://example.com)!',
        link_preview=False
    )

    # Sending a message returns the sent message object, which you can use
    print(message.raw_text)
    # You can reply to messages directly if you have a message object
    await message.reply('Cool!')

    # Or send files, songs, documents, albums...
    # await client.send_file('me', '/home/me/Pictures/holidays.jpg')

    # You can print the message history of any chat:
    async for message in client.iter_messages('me'):
        print(message.id, message.text)

        # You can download media from messages, too!
        # The method will return the path where the file was saved.
        if message.photo:
            path = await message.download_media()
            print('File saved to', path)  # printed after download is done


async def search():
    last_message = (await client.get_messages(-1001421875046, 1))[0]
    print(last_message.document.attributes[0].performer, last_message.text)


with client:
    client.loop.run_until_complete(main())
