import time
import json 

from telethon import TelegramClient

from shared.constants import TELEGRAM_API_ID, TELEGRAM_API_HASH

CHANNELS_TRAIN = ['Телеграмма РЖД']
CHANNELS_CAR = ['АВТО БАТЯ']
CHANNELS_AIR = ['АЭРОФЛОТ']
PARSING_CHANNELS_NAMES = [*CHANNELS_TRAIN, *CHANNELS_CAR, *CHANNELS_AIR]

MS_DELAY_BEFORE_NEXT_MESSAGE = 1
MAX_MESSAGES = 1_500
OUTPUT_FILE = 'data.json'

client = TelegramClient('tg_parser', TELEGRAM_API_ID, TELEGRAM_API_HASH)
    
async def main():
    await client.get_me()
    
    dialogs = await client.get_dialogs()
    data = {}

    for dialog in dialogs:
        if dialog.title in PARSING_CHANNELS_NAMES:
            messages = client.iter_messages(dialog)
            messages_list = []
            
            print(f'[status]: {dialog.title} parsing start!')
            
            async for message in messages:
                if (message.text != '' or message.text != ' '):
                    messages_list.append(message.text)
                    
                    print(f'[parse] {dialog.title} - {len(messages_list)}: {message.text}')
                
                if (len(messages_list) >= MAX_MESSAGES):
                    break
                
                time.sleep(MS_DELAY_BEFORE_NEXT_MESSAGE)      
                
            data[dialog.title] = messages_list
            
            print(f'[status]: {dialog.title} parsing end!')
            
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
                
with client:
    client.loop.run_until_complete(main())