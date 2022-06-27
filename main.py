import os
from flask import Flask, render_template, request, redirect, send_file
from s3_functions import upload_file, download_file
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
BUCKET = "pricetrackadya"


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        upload_file(f"uploads/{f.filename}", BUCKET)
        redirect("/")


@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


if __name__ == '__main__':
    app.run()
