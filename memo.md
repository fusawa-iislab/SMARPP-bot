最終的にはhttpでdeploy

```python
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv
import os

# .env 読み込み
load_dotenv()

# Slack App 初期化（Events API 用）
slack_app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
    process_before_response=True  # 非同期処理のために推奨
)

# イベント受信処理
@slack_app.message("")
def handle_any_message(message, say):
    user = message.get("user")
    text = message.get("text")
    say(f"<@{user}> さん、メッセージありがとう！: {text}")

# Flask アプリ
app = Flask(__name__)
handler = SlackRequestHandler(slack_app)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# 開発用の実行
if __name__ == "__main__":
    app.run(port=3000)
```