from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeSticker
import configparser
# Replace these with your own details
# api_id = ''  # Get it from my.telegram.org
# api_hash = ''  # Get it from my.telegram.org
# # Your phone number with the country code (e.g., +1 for USA)
# phone_number = ''
# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone_number = config['Telegram']['phone']
username = config['Telegram']['username']
# Initialize the client
client = TelegramClient('session_name', api_id, api_hash)


async def main():
    # Log in to your Telegram account
    await client.start(phone_number)

    # Replace 'group_name' with the actual name of the group you want to track
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        print(dialog.name, dialog.id)
    group = await client.get_entity(-4760779711)
    print(group)
    print(f'Listening for stickers in {group.title}...')

    # Define the event handler for new messages
    @client.on(events.NewMessage(chats=group))
    async def handler(event):
        if event.message.sticker:  # Check if the message contains a sticker
            sticker = event.message.sticker
            # print(sticker)
            # Access the sticker attribute
            document = sticker
            sticker_v = None
            for attribute in document.attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    sticker_v = attribute
                    break
            # print(sticker_v)
            # Example: Check if sticker emoji matches '⬆️' or '⬇️'
            tmp_emoji = sticker_v.alt
            if tmp_emoji == '💹':
                print(f"Up signal {tmp_emoji} from {group.title}")
            elif tmp_emoji == '📉':
                print(f"Down signal {tmp_emoji} from {group.title}")

    # Run the client to listen for new messages
    await client.run_until_disconnected()

# Run the main function
client.loop.run_until_complete(main())
