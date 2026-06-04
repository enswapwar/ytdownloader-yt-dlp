from flask import Flask, request, jsonify, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URLがありません"}), 400

    uid = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_DIR, f"{uid}.%(ext)s")

    try:
        subprocess.run(
            [
                "yt-dlp",
                "-o",
                output_template,
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
            return jsonify({"error": "ダウンロード失敗"}), 500

        return send_file(
            files[0],
            as_attachment=True
        )

    except subprocess.CalledProcessError:
        return jsonify({"error": "yt-dlpエラー"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
