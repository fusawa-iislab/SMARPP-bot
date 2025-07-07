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

persons = [
    {
        "name": "p1",
        "persona": "user同様の悩みを打ち明ける参加者",
    },
    {
        "name": "p2",
        "persona": "親身に相談に乗るカウンセラー",
    },
]

def generate_developer_prompt(name: str, persona: str) -> str:
    return {
        "role": "developer", 
        "content": (
            "ここでは集団でのカウンセリングが行われています。" +
            f"あなたは{persona}である{name}です。" +
            "会話の流れに合うように応答してください。" +
            "[]での人の名前を出さなくても大丈夫です。"
        )
    }

def generate_conversation_log_item(name: str, content: str) -> dict:
    return {
        "role": "user",
        "content": f"[{name}] {content}"
    }


## 0番目にはdeveloperのプロンプトを入れる
conversation_log = [None]



@slack_app.message("")
def handle_message_events(message, say, client):
    # user_id = message.get("user")
    # user_info = client.users_info(user=user_id)
    # if user_info["ok"]:
    #     username = user_info["user"]["real_name"]
    #     print(username)
    user_text = message.get('text', '')
    message_data = format_chatlog(message)
    conversation_log.append(generate_conversation_log_item("user", user_text))
    # save_chatlog(message_data)
    for person in persons:
        conversation_log[0] = generate_developer_prompt(**person)
        response_text = get_response(conversation_log, model="gpt-4o")
        response = p1.response(channel=message['channel'], text=response_text)
        response_data = format_chatlog(response)
        conversation_log.append(generate_conversation_log_item(person['name'], response_text))
    # save_chatlog(response_data)
    logging.info(f"Message successfully processed")
    print(conversation_log)



if __name__ == "__main__":
    SocketModeHandler(slack_app, os.getenv("APP_LEVEL_TOKEN")).start()