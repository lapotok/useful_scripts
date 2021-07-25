# https://habr.com/ru/post/425151/

from telethon import TelegramClient, sync

# Вставляем api_id и api_hash из https://my.telegram.org/
api_id = '...'
api_hash = '...'

client = TelegramClient('session_name', api_id, api_hash)
client.start()

#print(client.get_me().stringify())

client.send_message('usr', 'msg')
