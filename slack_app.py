from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os

load_dotenv(dotenv_path="./.botinfo")

slack_app = App(
    token=os.getenv("BOT_USER_OAUTH_TOKEN"),
    signing_secret=os.getenv("SIGNING_SECRET"),
)


@slack_app.message("")
def handle_message_events(message, say):
    print(1)
    user_text = message.get('text', '')
    say(f"受け取りました: {user_text}")

if __name__ == "__main__":
    SocketModeHandler(slack_app, os.getenv("APP_LEVEL_TOKEN")).start()