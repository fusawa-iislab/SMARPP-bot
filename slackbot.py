from slack_sdk import WebClient
import json

class Slackbot:
    def __init__(self, json_filepath: str):
        with open(json_filepath, 'r') as file:
            config = json.load(file)
        self.bot_user_oauth_token = config.get("BOT_USER_OAUTH_TOKEN")
        self.client_id = config.get("CLIENT_ID")
        self.client_secret = config.get("CLIENT_SECRET")
        self.signing_secret = config.get("SIGNING_SECRET")
        self.verification_token = config.get("VERIFICATION_TOKEN")
        self.app_level_token = config.get("APP_LEVEL_TOKEN")
        self.persona = ""
        self.name = ""

    @property
    def client(self):
        if not self.bot_user_oauth_token:
            raise ValueError("BOT_USER_OAUTH_TOKEN is not set in the environment variables.")
        return WebClient(token=self.bot_user_oauth_token)

    def response(self, channel: str, text: str):
        if not self.client:
            raise ValueError("Slack client is not initialized.")
        return self.client.chat_postMessage(channel=channel, text=text)


        
