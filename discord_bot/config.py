import os

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
# CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
CHANNEL_ID = None
channel_id_str = os.getenv('CHANNEL_ID')
if channel_id_str:
    try:
        CHANNEL_ID = int(channel_id_str)
    except ValueError:
        print("Error: CHANNEL_ID in .env file must be an integer.")

if CHANNEL_ID is None:  
    print("Error: CHANNEL_ID not found in .env file.")
    # You could also raise an exception here if you want the program to stop


