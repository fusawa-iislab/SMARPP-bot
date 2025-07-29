from typing import Sequence

from ChatRoom import ChatRoom
from ChatData import ChatData
from Slackbot import Slackbot

def chatlog_prompt(chatdatas: Sequence[ChatData]) -> str:
    return "\n".join(f"[{chatdata.name}] {chatdata.content}" for chatdata in chatdatas)

def environment_prompt(user_name: str, chatbots: dict[str, Slackbot]) -> str:
    person_name_list = [user_name] + [bot.name for bot in chatbots.values()]
    person_names = ", ".join(person_name_list)
    faci_bot = next((bot for bot in chatbots.values() if bot.is_facilitator), None)
    return (
        "ここでは集団でのカウンセリングが行われています。"
        f"参加者は{person_names}で、ファシリテータは{faci_bot.name}です。\n"
    )

def personality_prompt(p: Slackbot) -> str:
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
    return personal_text

def user_prompt(chatroom: ChatRoom, p: Slackbot, username: str, additional_prompt: str | None = None) -> str:
    return (
        f"{environment_prompt(username, chatroom.chatbots)}"
        f"これまでの会話の流れ: \n"
        f"{chatlog_prompt(chatroom.chatdatas)}\n"
        f"{personality_prompt(p)}"
        "これまでの会話の流れに沿って応答してください。\n"
        "※人の名前が書いてある[]は出さないでください\n"
        f"{additional_prompt}\n"
    )

def create_prompt(chatroom: ChatRoom, p: Slackbot, username: str, additional_prompt: str | None = None):
    return [
        {
            "role": "user",
            "content": user_prompt(chatroom, p, username, additional_prompt)
        }
    ]