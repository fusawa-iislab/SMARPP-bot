from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import logging
from typing import Sequence

from llm import get_response
from utils import format_chatlog
from Slackbot import Slackbot
from firebase.models import save_chatlog

peer_1 = Slackbot("./.botinfo/peer-1.json")
faci_bot = Slackbot("./.botinfo/faci-bot.json")
p1 = Slackbot("./.botinfo/p1.json")

load_dotenv(dotenv_path="./.botinfo/test1")

slack_app = App(
    token=os.getenv("BOT_USER_OAUTH_TOKEN"),
    signing_secret=os.getenv("SIGNING_SECRET"),
)

faci_bot.persona = "ファシリテーター"
faci_bot.name = "ファシ田"
faci_bot.is_facilitator = True

peer_1.persona = "user同様の悩みを抱える参加者"
peer_1.name = "参加者1"

chatbots = [faci_bot, peer_1]


#faci_botの情報を関数外から取ってる
def generate_enviroment_prompt(username: str ,chatbots: Sequence[Slackbot]) -> str:
    person_name_list = [username] + [bot.name for bot in chatbots]
    person_names = ", ".join(person_name_list)

    return (
        "ここでは集団でのカウンセリングが行われています。"
        f"参加者は{person_names}で、ファシリテータは{faci_bot.name}です。\n" 
    )

def generate_personal_prompt(p: Slackbot) -> str:
    personal_text = f"あなたは{p.persona}である{p.name}です。\n" 
    if p.is_facilitator:
        personal_text += (
            "あなたはファシリテーターとして、以下の流れに沿ってセッションを進めていきます\n"
            "その流れの中で特に深掘った方がいいことや悩みの相談は特に聞くこと\n"
            "セッションの流れ:\n"
            "1. 参加者の最近の様子を聞く/薬物使用状況や生活の悩み、よかったこと\n"
            "2. 今後直近の生活をどうしていきたいか\n"
            "\n"
        )
    situational_text = (
        "会話の流れに合うように応答してください。\n" 
        "注意事項:\n" 
        "[]での人の名前を出さないでください。\n"
    )
    return (
        personal_text + situational_text
    )

def generate_developer_prompt(username: str,chatbot: Slackbot) -> dict:
    return {
        "role": "developer",
        "content": (
            generate_enviroment_prompt(username, chatbots) +
            generate_personal_prompt(chatbot)
        )
    }

def generate_user_prompt(chatlog) -> dict:
    return {
        "role": "user",
        "content": (
            "以下の会話の流れに沿うように応答してください\n" +
            "会話の流れ:\n" +
            f"{chatlog}\n"
        )
    }


chatlog = ""
def chatlog_item(name: str, content: str) -> str:
    return f"[{name}]: {content}\n"
    

@slack_app.event("message")
def handle_message_events(message, say, client):
    global chatlog
    if message.get("bot_id"):
        logging.info("Ignoring message from bot")
        return
    # user_id = message.get("user")
    # user_info = client.users_info(user=user_id)
    # if user_info["ok"]:
    #     username = user_info["user"]["real_name"]
    #     print(username)
    user_text = message.get('text', '')
    chatlog+=chatlog_item("user", user_text)
    message_data = format_chatlog(message)
    # save_chatlog(message_data)
    for chatbot in chatbots:
        prompts = []
        prompts.append(generate_developer_prompt("user", chatbot))
        prompts.append(generate_user_prompt(chatlog))
        response_text = get_response(prompts, model="gpt-4o")
        response = chatbot.response(channel=message['channel'], text=response_text)
        chatlog+=chatlog_item(chatbot.name, response_text)
        response_data = format_chatlog(response)
        # save_chatlog(response_data)
    logging.info(f"Message successfully processed")
    # print(conversation_log)



if __name__ == "__main__":
    SocketModeHandler(slack_app, os.getenv("APP_LEVEL_TOKEN")).start()