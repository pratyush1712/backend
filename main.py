import os
from flask import Flask, render_template, request, redirect, send_file
from backend.scraper import Scraper
from s3_functions import upload_file, download_file
from werkzeug.utils import secure_filename
import json
import requests
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
BUCKET = "pricetrackadya"


@app.route("/parse", methods=["POST"])
def parse():
    body = json.loads(request.data)
    file_url = body.get("url")
    store = body.get("store")
    in_col_header = body.get("in_col")
    sheet = body.get("sheet")
    out_col_header = body.get("out_col")
    if (file_url is None or store is None or in_col_header is None or out_col_header is None or sheet is None):
        return failure_response("invalid params supplied")
    try:
        file = requests.get(file_url)
        file_name = uuid.uuid4()
        open(file_name 'wb').write(r.content)

    except Exception as e:
        return failure_response(str(e))
    scraper = Scraper()


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
    app.run(host="localhost", port=8000, debug=True)
