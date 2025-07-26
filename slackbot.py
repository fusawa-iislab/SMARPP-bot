from slack_sdk import WebClient

class Slackbot:
    def __init__(
            self,
            bot_user_oauth_token: str | None = None,
            client_id: str | None = None,
            client_secret: str | None = None,
            signing_secret: str | None = None,
            verification_token: str | None = None,
            app_level_token: str | None = None,
            persona: str | None = None,
            name: str | None = None,
            is_facilitator: bool = False,
        ):
        self.bot_user_oauth_token = bot_user_oauth_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.signing_secret = signing_secret
        self.verification_token = verification_token
        self.app_level_token = app_level_token
        self.persona = persona
        self.name = name
        self.is_facilitator = is_facilitator

    def __repr__(self):
        return f"Slackbot(name={self.name}, persona={self.persona}, is_facilitator={self.is_facilitator} bot_user_oauth_token={self.bot_user_oauth_token} client_id={self.client_id} client_secret={self.client_secret} signing_secret={self.signing_secret} verification_token={self.verification_token} app_level_token={self.app_level_token})"

    @property
    def client(self):
        if not self.bot_user_oauth_token:
            raise ValueError("BOT_USER_OAUTH_TOKEN is not set in the environment variables.")
        return WebClient(token=self.bot_user_oauth_token)

    def response(self, channel: str, text: str):
        if not self.client:
            raise ValueError("Slack client is not initialized.")
        return self.client.chat_postMessage(channel=channel, text=text)



        
