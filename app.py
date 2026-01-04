from flask import Flask, Response, request, render_template
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

@app.route("/")
def home():
    return "CinemaHub Streaming Server Running"

@app.route("/watch/<path:file_path>")
def watch(file_path):
    return render_template(
        "watch.html",
        stream_url=f"/stream/{file_path}"
    )

@app.route("/stream/<path:file_path>")
def stream(file_path):
    tg_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    headers = {}
    range_header = request.headers.get("Range")
    if range_header:
        headers["Range"] = range_header

    r = requests.get(tg_url, headers=headers, stream=True)

    def generate():
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                yield chunk

    response = Response(
        generate(),
        status=r.status_code,
        content_type="video/mp4"
    )

    # IMPORTANT HEADERS
    if "Content-Range" in r.headers:
        response.headers["Content-Range"] = r.headers["Content-Range"]
    if "Content-Length" in r.headers:
        response.headers["Content-Length"] = r.headers["Content-Length"]

    response.headers["Accept-Ranges"] = "bytes"

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)