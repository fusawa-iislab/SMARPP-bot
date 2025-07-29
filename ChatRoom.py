from typing import Sequence
from ChatData import ChatData
from Slackbot import Slackbot

class ChatRoom:
    def __init__(self, channel_id: str| None = None, chatdatas: Sequence[ChatData] = [], chatbots: dict[str, Slackbot] = {}, is_active: bool = False):
        self.channel_id = channel_id
        self.chatdatas = chatdatas
        self.chatbots = chatbots
        self.faci_bot = next((bot for bot in chatbots.values() if bot.is_facilitator), None)
        self.is_active = is_active
        if self.faci_bot is None:
            raise ValueError("ファシリテーターが見つかりません。必ず追加してください")

    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "chatdatas": [chatdata.to_dict() for chatdata in self.chatdatas]
        }

    def add_chatdata(self, name: str, content: str):
        self.chatdatas.append(ChatData(self.channel_id, name, content))
        return
