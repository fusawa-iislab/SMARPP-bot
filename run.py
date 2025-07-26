from dotenv import load_dotenv
import argparse
import os
from slack_app import create_slack_app
from slack_bolt.adapter.socket_mode import SocketModeHandler
from Slackbot import Slackbot
from fastapi_app import create_fastapi_app
import uvicorn

load_dotenv()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Slack app.")
    parser.add_argument("-l", "--local", action="store_true", help="run in local mode")
    args = parser.parse_args()

    if args.local:
        slack_app = create_slack_app(
            token=os.getenv("LOCAL_BOT_USER_OAUTH_TOKEN"),
            signing_secret=os.getenv("LOCAL_SIGNING_SECRET"),
        )
        handler = SocketModeHandler(slack_app, os.getenv("LOCAL_APP_LEVEL_TOKEN"))
        handler.start()
    else:
        slack_app = create_slack_app(
            token=os.getenv("BOT_USER_OAUTH_TOKEN"),
            signing_secret=os.getenv("SIGNING_SECRET"),
        )
        fastapi_app = create_fastapi_app(slack_app)
        uvicorn.run(
            fastapi_app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8080)),
        )


