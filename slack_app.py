from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import logging

from utils import format_chatlog
from slackbot import Slackbot
from firebase.models import save_chatlog

p1 = Slackbot("./.botinfo/p1")

load_dotenv(dotenv_path="./.botinfo/test1")

slack_app = App(
    token=os.getenv("BOT_USER_OAUTH_TOKEN"),
    signing_secret=os.getenv("SIGNING_SECRET"),
)


@slack_app.message("")
def handle_message_events(message, say, client):
    # user_id = message.get("user")
    # user_info = client.users_info(user=user_id)
    # if user_info["ok"]:
    #     username = user_info["user"]["real_name"]
    #     print(username)
    user_text = message.get('text', '')
    message_data = format_chatlog(message)
    save_chatlog(message_data)
    # print(message)
    # print(message_data)
    response = p1.response(channel=message['channel'], text=user_text + "this is test")
    response_data = format_chatlog(response)
    save_chatlog(response_data)
    # print(response)
    # print(response_data)
    logging.info(f"Message successfully processed")


if __name__ == "__main__":
    SocketModeHandler(slack_app, os.getenv("APP_LEVEL_TOKEN")).start()