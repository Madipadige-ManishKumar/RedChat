import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from src.agents.executor import run_agent
from src.config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN # Add these to your config.py

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def handle_app_mentions(event, say):
    """Handles cases where the bot is mentioned in a channel (@bot-name)"""
    user_query = event["text"]
    thread_ts = event.get("thread_ts", event["ts"])
    
    print(user_query,"This is the query")
    # Optional: Visual "Thinking" indicator
    print(f"Processing Slack Mention: {user_query}")
    
    try:
        # Call your existing Gemini agent logic
        response = run_agent(user_query)
        
        # Reply in the same thread
        say(text=response, thread_ts=thread_ts)
    except Exception as e:
        say(text=f"❌ Error: {str(e)}", thread_ts=thread_ts)

@app.event("message")
def handle_message_events(event, say):
    """Handles Direct Messages (DMs) to the bot"""
    # Only respond to DMs (channel type 'im') to avoid infinite loops in public channels
    if event.get("channel_type") == "im":
        user_query = event["text"]
        response = run_agent(user_query)
        say(text=response)

if __name__ == "__main__":
    print("⚡️ Redshotlabs Agent is running on Slack (Socket Mode)!")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()