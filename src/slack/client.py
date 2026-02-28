# src/slack/client.py
from slack_bolt import App
from slack_sdk import WebClient
from src.config import SLACK_BOT_TOKEN

# Shared client for all tools
client = WebClient(token=SLACK_BOT_TOKEN) 
# Bolt App for the main listener
app = App(token=SLACK_BOT_TOKEN)