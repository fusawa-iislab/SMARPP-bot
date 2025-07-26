from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from slack_bolt.adapter.fastapi import SlackRequestHandler

def create_fastapi_app(slack_app) -> FastAPI:
    fastapi_app = FastAPI()
    handler = SlackRequestHandler(slack_app)

    @fastapi_app.get("/", response_class=HTMLResponse)
    async def root():
        html_content = """
        <html>
            <head>
                <title>Slack Bot Status</title>
            </head>
            <body>
                <h1>Slack Bot is Running!</h1>
                <p>ここはデバッグ用の簡単な画面です。</p>
            </body>
        </html>
        """
        return html_content

    @fastapi_app.post("/slack/events")
    async def slack_events(request: Request):
        body = await request.json()
        print("fast_api reveive")
        # 👇 challenge に対応
        if body.get("type") == "url_verification":
            return {"challenge": body.get("challenge")}
        return await handler.handle(request)

    return fastapi_app

