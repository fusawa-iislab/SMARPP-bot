def format_chatlog(input: dict):
    is_bot = input.get("message", {} ).get("bot_profile", None) is not None
    if is_bot:
        message = input.get("message", {})
        content = message.get("text", "")
        agent_id = message.get("bot_profile", {}).get("id", "")
        agent_name = message.get("bot_profile", {}).get("name", None)
    else:
        content = input.get("text", "")
        agent_id = input.get("user", "")
        agent_name = None

    return {
        "timestamp": input.get("ts", ""),
        "channel_id": input.get("channel", ""),
        "is_bot": is_bot,
        "content": content,
        "agent_id": agent_id,
        "agent_name": agent_name,
    }