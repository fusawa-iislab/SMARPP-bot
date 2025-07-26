from slack_bolt import App 
from slack_bolt.adapter.socket_mode import SocketModeHandler
import logging

from llm import get_response
from utils import format_chatlog
from ChatRoom import ChatRoom
from Slackbot import Slackbot
from firebase.models import save_chatlog
from prompt import create_prompt
from dotenv import load_dotenv
import os

load_dotenv()

def get_chatbots():
    peer_1 = Slackbot(
        bot_user_oauth_token=os.getenv("PEER_1_BOT_USER_OAUTH_TOKEN"),
        client_id=os.getenv("PEER_1_CLIENT_ID"),
        client_secret=os.getenv("PEER_1_CLIENT_SECRET"),
        signing_secret=os.getenv("PEER_1_SIGNING_SECRET"),
        verification_token=os.getenv("PEER_1_VERIFICATION_TOKEN"),
    )
    faci_bot = Slackbot(
        bot_user_oauth_token=os.getenv("FACI_BOT_BOT_USER_OAUTH_TOKEN"),
        client_id=os.getenv("FACI_BOT_CLIENT_ID"),
        client_secret=os.getenv("FACI_BOT_CLIENT_SECRET"),
        signing_secret=os.getenv("FACI_BOT_SIGNING_SECRET"),
        verification_token=os.getenv("FACI_BOT_VERIFICATION_TOKEN"),
    )
    p1 = Slackbot(
        bot_user_oauth_token=os.getenv("P1_BOT_USER_OAUTH_TOKEN"),
        client_id=os.getenv("P1_CLIENT_ID"),
        client_secret=os.getenv("P1_CLIENT_SECRET"),
        signing_secret=os.getenv("P1_SIGNING_SECRET"),
        verification_token=os.getenv("P1_VERIFICATION_TOKEN"),
    )

    faci_bot.persona = "ファシリテーター"
    faci_bot.name = "ファシ田"
    faci_bot.is_facilitator = True


    peer_1.persona = "user同様の悩みを抱える参加者"
    peer_1.name = "参加者1"

    return [faci_bot, peer_1]


def create_slack_app(token: str, signing_secret: str) :
    app = App(token=token, signing_secret=signing_secret)
    username = "yugo"
    chatroom = ChatRoom()
    app.chatbots = get_chatbots()
    chatroom.chatbots = app.chatbots

    @app.event("message")
    def handle_message_events(message, say, client):
        if message.get("bot_id"):
            logging.info("Ignoring message from bot")
            return
        user_text = message.get('text', '')
        chatroom.add_chatdata(username, user_text)
        message_data = format_chatlog(message)
        # save_chatlog(message_data)

        for chatbot in app.chatbots:
            prompt = create_prompt(chatroom, chatbot, username)
            response_text = get_response(prompt, model="gpt-4o")
            response = chatbot.response(channel=message['channel'], text=response_text)
            chatroom.add_chatdata(chatbot.name, response_text)
            response_data = format_chatlog(response)
            # save_chatlog(response_data)

        logging.info("Message successfully processed")

    return app
