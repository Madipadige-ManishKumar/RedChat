import slack 
import os 
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("slack_outh_token")

client = slack.WebClient(token=token)


client.chat_postMessage(channel="#general",text="Hello world This is message coming  from the python code ")
