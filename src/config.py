import os 
from dotenv import load_dotenv
load_dotenv()

SLACK_BOT_TOKEN = os.getenv("slack_outh_token")
SLACK_APP_TOKEN = os.getenv("slack_app_token")
GEMINI_API_KEY = os.getenv("apikey");

MODEL_ID = "gemini-3-flash-preview"

CHROME_PATH="./chromeDB"
EMBEDDING_MODEL = "all-MiniLM-L6-v2" #

