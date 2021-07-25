#!/usr/bin/python

# from @BotFather, /newbot
TELEGRAM_TOKEN = '...'
# from https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates
TELEGRAM_CHAT_ID = '...'

import requests
import sys

payload = {
	'chat_id': TELEGRAM_CHAT_ID,
	'text': sys.argv[1],
	'parse_mode': 'HTML'
}
requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN),
							 data=payload)
