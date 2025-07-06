from dotenv import load_dotenv
import os
from slack_sdk import WebClient


class Slackbot:
    def __init__(self, filepath: str):
        load_dotenv(dotenv_path=filepath)
        self.bot_user_oauth_token = os.getenv("BOT_USER_OAUTH_TOKEN") or None
        self.client_id = os.getenv("CLIENT_ID") or None
        self.client_secret = os.getenv("CLIENT_SECRET") or None
        self.signing_secret = os.getenv("SIGNING_SECRET") or None
        self.verification_token = os.getenv("VERIFICATION_TOKEN") or None
        self.app_level_token = os.getenv("APP_LEVEL_TOKEN") or None
        self.persona = ""

    @property
    def client(self):
        if not self.bot_user_oauth_token:
            raise ValueError("BOT_USER_OAUTH_TOKEN is not set in the environment variables.")
        return WebClient(token=self.bot_user_oauth_token)

    def response(self, channel: str, text: str):
        if not self.client:
            raise ValueError("Slack client is not initialized.")
        return self.client.chat_postMessage(channel=channel, text=text)


        
