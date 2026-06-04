from flask import Flask, request, jsonify, send_file, send_from_directory
import subprocess
import os
import uuid

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def index():
    return send_file(os.path.join(ROOT_DIR, "index.html"))

@app.route("/programfile/<path:filename>")
def programfile(filename):
    return send_from_directory(BASE_DIR, filename)

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({
            "success": False,
            "error": "URLが指定されていません"
        }), 400

    uid = str(uuid.uuid4())

    template = os.path.join(
        DOWNLOAD_DIR,
        f"{uid}.%(ext)s"
    )

    try:
        subprocess.run(
            [
                "yt-dlp",
                "-o",
                template,
                url
            ],
            check=True
        )

        files = [
            os.path.join(DOWNLOAD_DIR, f)
            for f in os.listdir(DOWNLOAD_DIR)
            if f.startswith(uid)
        ]

        if not files:
            return jsonify({
                "success": False,
                "error": "ファイルが見つかりません"
            }), 500

        filepath = files[0]

        response = send_file(
            filepath,
            as_attachment=True
        )

        @response.call_on_close
        def cleanup():
            try:
                os.remove(filepath)
            except:
                pass

        return response

    except subprocess.CalledProcessError:
        return jsonify({
            "success": False,
            "error": "yt-dlp実行失敗"
        }), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
