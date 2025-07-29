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

    return {
        "faci_bot": faci_bot,
        "peer_1": peer_1,
    }


def create_slack_app(token: str, signing_secret: str) :
    app = App(token=token, signing_secret=signing_secret)
    username = "yugo"
    app.chatrooms = []
    app.chatbots = get_chatbots()

    @app.event("message")
    def handle_message_events(message, say, client):
        if message.get("bot_id"):
            logging.info("Ignoring message from bot")
            return
        user_text = message.get('text', '')
        chatroom = next((chatroom for chatroom in app.chatrooms if chatroom.channel_id == message['channel']), None)
        if chatroom is None:
            chatroom = ChatRoom(message['channel'], chatbots=app.chatbots)
            app.chatrooms.append(chatroom)
        if user_text in ["start", "スタート"]:
            if chatroom.is_active:
                say("すでにセッションが開始されています。")
                return
            chatroom.is_active = True
            say("セッションを開始します。")
            prompt = create_prompt(chatroom, app.chatbots["faci_bot"], username, "セッションが開始されたので、セッションの流れを開始してください。初めはuserに話を振ってください")
            response_text = get_response(prompt, model="gpt-4o")
            response = app.chatbots["faci_bot"].response(channel=message['channel'], text=response_text)
            chatroom.add_chatdata(app.chatbots["faci_bot"].name, response_text)
            response_data = format_chatlog(response)
            # save_chatlog(response_data)

        elif user_text in ["end", "終了"]:
            if not chatroom.is_active:
                say("セッションが開始されていません。")
                return
            chatroom.is_active = False
            say("セッションを終了します。")
        elif not chatroom.is_active:
            say("セッションが開始されていません。開始するには「start」と入力してください。")
            return
        else:
            chatroom.add_chatdata(username, user_text)
            message_data = format_chatlog(message)
            # save_chatlog(message_data)

            for chatbot in app.chatbots.values():
                prompt = create_prompt(chatroom, chatbot, username)
                response_text = get_response(prompt, model="gpt-4o")
                response = chatbot.response(channel=message['channel'], text=response_text)
                chatroom.add_chatdata(chatbot.name, response_text)
                response_data = format_chatlog(response)
                # save_chatlog(response_data)

        logging.info("Message successfully processed")

    return app
