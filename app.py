from flask import Flask, Response
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

@app.route("/")
def home():
    return "CinemaHub Streaming Server Running"

@app.route("/watch/<path:file_path>")
def watch(file_path):
    tg_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    def generate():
        with requests.get(tg_url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    yield chunk

    return Response(generate(), content_type="video/mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)