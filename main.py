import asyncio
from telethon import TelegramClient
import os
import configparser



async def main():
    config = configparser.ConfigParser()
    config.read('data/config.ini')

    #Настривается в config.ini
    api_id = config.getint('DEFAULT', 'api_id')
    api_hash = config.get('DEFAULT', 'api_hash')

    # имя сессии
    session = 'data/parsing'

    client = TelegramClient(session, api_id, api_hash)
    
    await client.start()
    folder = os.path.dirname(os.path.abspath(__file__)) 
    filepath = os.path.join(folder, "channel.txt")
    
    try:
        with open(filepath, 'w+', encoding='utf-8') as file:
            dialogs = await client.get_dialogs()
            for dialog in dialogs:
                if dialog.is_channel:
                    entity = await client.get_entity(dialog.id)
                    if entity.username:
                        channel_link = f"https://t.me/{entity.username}"
                    else:
                        channel_link = f"Закрытый канал"
                    if channel_link == 'Закрытый канал':
                        file.write(f'{dialog.title} - {channel_link}\n')
                        print(f'{dialog.title} - {channel_link}')
                    else:
                        file.write(f'{channel_link}\n')
                        print(f'{channel_link}')
    finally:
        file.close()

    
    await client.disconnect()

asyncio.run(main())
