class ChatData:
    def __init__(self, channel_id: str, name: str, content: str):
        self.channel_id = channel_id
        self.name = name
        self.content = content

    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "name": self.name,
            "content": self.content
        }