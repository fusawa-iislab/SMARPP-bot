from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import logging

from llm import get_response
from utils import format_chatlog
from Slackbot import Slackbot
from firebase.models import save_chatlog

p1 = Slackbot("./.botinfo/p1")

load_dotenv(dotenv_path="./.botinfo/test1")

slack_app = App(
    token=os.getenv("BOT_USER_OAUTH_TOKEN"),
    signing_secret=os.getenv("SIGNING_SECRET"),
)

p1.persona = "あなたは、会話相手の相談に乗るカウンセラーです。会話の流れに合うように応答してください"
conversation_log = [
    {
        "role" : "developer",
        "content" : p1.persona
    }
    ,
    {
        "role": "user",
        "content": "こんにちは、今日はどんなことを話しましょうか？"
    },
    {
        "role": "assistant",
        "content": "こんにちは！今日はどんなことを話したいですか？" 
    },
]


@slack_app.message("")
def handle_message_events(message, say, client):
    # user_id = message.get("user")
    # user_info = client.users_info(user=user_id)
    # if user_info["ok"]:
    #     username = user_info["user"]["real_name"]
    #     print(username)
    user_text = message.get('text', '')
    message_data = format_chatlog(message)
    conversation_log.append(
        {
            "role": "user",
            "content": user_text
        }
    )
    # save_chatlog(message_data)
    response_text = get_response(conversation_log, model="gpt-4o")
    response = p1.response(channel=message['channel'], text=response_text)
    response_data = format_chatlog(response)
    conversation_log.append(
        {
            "role": "assistant",
            "content": response_text,
        }
    )
    # save_chatlog(response_data)
    logging.info(f"Message successfully processed")


if __name__ == "__main__":
    SocketModeHandler(slack_app, os.getenv("APP_LEVEL_TOKEN")).start()