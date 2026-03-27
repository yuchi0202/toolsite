from flask import Flask, request, send_file
import random
import string
import base64
import urllib.parse
import time
import datetime
import uuid
import hashlib
import json
import io
import html
import zipfile

from PIL import Image
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

app = Flask(__name__)

BOOTSTRAP = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<meta name="viewport" content="width=device-width, initial-scale=1">
"""

def h(v):
    return html.escape("" if v is None else str(v))

def layout(title, content):
    return f"""
    <html>
    <head>
        <title>{title}</title>
        {BOOTSTRAP}
    </head>
    <body class="bg-light">

    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">My Tool Site 工具網站</a>
        </div>
    </nav>

    <div class="container py-5">
        <h1 class="mb-4">{title}</h1>
        {content}
        <br>
        <a href="/" class="btn btn-dark">Home 首頁</a>
    </div>

    <footer class="text-center text-muted py-4">
        Free Online Tools © 2026
    </footer>

    </body>
    </html>
    """

def tool_card(title, subtitle, link, color):
    return f"""
    <div class="col-md-4">
        <div class="card shadow-sm mb-4">
            <div class="card-body">
                <h5>{title}</h5>
                <p>{subtitle}</p>
                <a href="{link}" class="btn btn-{color}">Open</a>
            </div>
        </div>
    </div>
    """

# 首頁
@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <title>Free Online Tools</title>
        {BOOTSTRAP}
    </head>
    <body class="bg-light">

    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">My Tool Site 工具網站</a>
        </div>
    </nav>

    <div class="container py-5">
        <h1 class="text-center mb-4">Free Online Tools 免費工具</h1>

        <div class="row">
            {tool_card("QR Code", "QR Code 產生器", "/qr", "primary")}
            {tool_card("Password", "密碼產生器", "/password", "success")}
            {tool_card("Base64", "Base64 編碼解碼", "/base64tool", "warning")}
            {tool_card("URL Encode", "URL 編碼解碼", "/urltool", "info")}
            {tool_card("Timestamp", "時間戳轉換", "/timestamp", "secondary")}
            {tool_card("UUID", "UUID 產生器", "/uuidtool", "dark")}
            {tool_card("Hash", "Hash 產生器", "/hashtool", "danger")}
            {tool_card("JSON Formatter", "JSON 格式化", "/json", "success")}
            {tool_card("Word Counter", "字數計算", "/word", "info")}
            {tool_card("Image to JPG", "圖片轉 JPG", "/image-to-jpg", "primary")}
            {tool_card("Image to PNG", "圖片轉 PNG", "/image-to-png", "success")}
            {tool_card("Image Resize", "圖片縮放", "/image-resize", "warning")}
            {tool_card("Image Compress", "圖片壓縮", "/image-compress", "secondary")}
            {tool_card("PDF Merge", "PDF 合併", "/pdf-merge", "danger")}
            {tool_card("PDF Split", "PDF 分割", "/pdf-split", "secondary")}
            {tool_card("YouTube Thumbnail", "YouTube 縮圖下載", "/youtube-thumb", "dark")}
        </div>
    </div>
    </body>
    </html>
    """

# QR
@app.route("/qr")
def qr():
    text = request.args.get("text", "")
    return layout("QR Code Generator", f"""
    <form>
        <input class="form-control mb-3" name="text">
        <button class="btn btn-primary">Generate</button>
    </form>
    <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={h(text)}">
    """)

# Password
@app.route("/password")
def password():
    pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
    return layout("Password Generator", f"""
    <div class="card p-4">
        <h3>{pwd}</h3>
        <a href="/password" class="btn btn-success mt-3">Generate New</a>
    </div>
    """)

# Base64
@app.route("/base64tool")
def base64tool():
    text = request.args.get("text", "")
    encoded = ""
    decoded = ""
    if text:
        encoded = base64.b64encode(text.encode()).decode()
        try:
            decoded = base64.b64decode(text.encode()).decode()
        except:
            decoded = "Decode Error"

    return layout("Base64 Tool", f"""
    <form>
        <textarea class="form-control mb-3" name="text">{h(text)}</textarea>
        <button class="btn btn-warning">Convert</button>
    </form>
    Encoded:<br>{h(encoded)}<br><br>
    Decoded:<br>{h(decoded)}
    """)

# URL Encode
@app.route("/urltool")
def urltool():
    text = request.args.get("text", "")
    return layout("URL Encode Decode", f"""
    <form>
        <textarea class="form-control mb-3" name="text">{h(text)}</textarea>
        <button class="btn btn-info">Convert</button>
    </form>
    Encoded:<br>{urllib.parse.quote(text)}<br><br>
    Decoded:<br>{urllib.parse.unquote(text)}
    """)

# Timestamp
@app.route("/timestamp")
def timestamp():
    ts = request.args.get("ts", "")
    now = int(time.time())
    result = ""
    if ts:
        try:
            if len(ts) > 10:
                result = datetime.datetime.fromtimestamp(int(ts)/1000)
            else:
                result = datetime.datetime.fromtimestamp(int(ts))
        except:
            result = "Invalid"
    return layout("Timestamp Converter", f"""
    Current Timestamp: {now}
    <form>
        <input class="form-control mb-3" name="ts">
        <button class="btn btn-secondary">Convert</button>
    </form>
    Result: {result}
    """)

# UUID
@app.route("/uuidtool")
def uuidtool():
    return layout("UUID Generator", f"""
    <h3>{uuid.uuid4()}</h3>
    <a href="/uuidtool" class="btn btn-dark">Generate</a>
    """)

# Hash
@app.route("/hashtool")
def hashtool():
    text = request.args.get("text", "")
    md5 = hashlib.md5(text.encode()).hexdigest() if text else ""
    sha = hashlib.sha256(text.encode()).hexdigest() if text else ""
    return layout("Hash Generator", f"""
    <form>
        <input class="form-control mb-3" name="text">
        <button class="btn btn-danger">Generate</button>
    </form>
    MD5:<br>{md5}<br><br>
    SHA256:<br>{sha}
    """)

# JSON Formatter
@app.route("/json")
def jsontool():
    text = request.args.get("text", "")
    formatted = ""
    try:
        formatted = json.dumps(json.loads(text), indent=4)
    except:
        formatted = "Invalid JSON"

    return layout("JSON Formatter", f"""
    <form>
        <textarea class="form-control mb-3" name="text" rows="6">{h(text)}</textarea>
        <button class="btn btn-success">Format</button>
    </form>
    <pre>{formatted}</pre>
    """)

# Word Counter
@app.route("/word")
def word():
    text = request.args.get("text", "")
    count = len(text.split())
    chars = len(text)
    return layout("Word Counter", f"""
    <form>
        <textarea class="form-control mb-3" name="text" rows="5">{h(text)}</textarea>
        <button class="btn btn-info">Count</button>
    </form>
    Words: {count}<br>
    Characters: {chars}
    """)

# Image tools
@app.route("/image-to-jpg", methods=["GET","POST"])
def image_to_jpg():
    if request.method == "POST":
        file = request.files["image"]
        img = Image.open(file.stream).convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)
        return send_file(buf, mimetype="image/jpeg")
    return layout("Image to JPG", """
    <form method="POST" enctype="multipart/form-data">
        <input class="form-control mb-3" type="file" name="image">
        <button class="btn btn-primary">Convert</button>
    </form>
    """)

@app.route("/image-to-png", methods=["GET","POST"])
def image_to_png():
    if request.method == "POST":
        file = request.files["image"]
        img = Image.open(file.stream)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return send_file(buf, mimetype="image/png")
    return layout("Image to PNG", """
    <form method="POST" enctype="multipart/form-data">
        <input class="form-control mb-3" type="file" name="image">
        <button class="btn btn-success">Convert</button>
    </form>
    """)

@app.route("/image-resize", methods=["GET","POST"])
def image_resize():
    if request.method == "POST":
        file = request.files["image"]
        width = int(request.form["width"])
        height = int(request.form["height"])
        img = Image.open(file.stream)
        img = img.resize((width, height))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return send_file(buf, mimetype="image/png")
    return layout("Image Resize", """
    <form method="POST" enctype="multipart/form-data">
        <input class="form-control mb-2" type="file" name="image">
        <input class="form-control mb-2" name="width" placeholder="Width">
        <input class="form-control mb-2" name="height" placeholder="Height">
        <button class="btn btn-warning">Resize</button>
    </form>
    """)

@app.route("/image-compress", methods=["GET","POST"])
def image_compress():
    if request.method == "POST":
        file = request.files["image"]
        quality = int(request.form["quality"])
        img = Image.open(file.stream)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality)
        buf.seek(0)
        return send_file(buf, mimetype="image/jpeg")
    return layout("Image Compress", """
    <form method="POST" enctype="multipart/form-data">
        <input class="form-control mb-2" type="file" name="image">
        <input class="form-control mb-2" name="quality" placeholder="Quality 1-95">
        <button class="btn btn-secondary">Compress</button>
    </form>
    """)

# PDF tools
@app.route("/pdf-merge", methods=["GET","POST"])
def pdf_merge():
    if request.method == "POST":
        files = request.files.getlist("pdfs")
        merger = PdfMerger()
        for f in files:
            merger.append(f)
        buf = io.BytesIO()
        merger.write(buf)
        buf.seek(0)
        return send_file(buf, mimetype="application/pdf")
    return layout("PDF Merge", """
    <form method="POST" enctype="multipart/form-data">
        <input class="form-control mb-3" type="file" name="pdfs" multiple>
        <button class="btn btn-danger">Merge PDF</button>
    </form>
    """)

@app.route("/pdf-split", methods=["GET","POST"])
def pdf_split():
    if request.method == "POST":
        file = request.files["pdf"]
        reader = PdfReader(file)
        writer = PdfWriter()
        page_num = int(request.form["page"]) - 1
        writer.add_page(reader.pages[page_num])
        buf = io.BytesIO()
        writer.write(buf)
        buf.seek(0)
        return send_file(buf, mimetype="application/pdf")
    return layout("PDF Split", """
    <form method="POST" enctype="multipart/form-data">
        <input class="form-control mb-2" type="file" name="pdf">
        <input class="form-control mb-2" name="page" placeholder="Page number">
        <button class="btn btn-secondary">Split PDF</button>
    </form>
    """)

# YouTube Thumbnail
@app.route("/youtube-thumb")
def youtube_thumb():
    url = request.args.get("url", "")
    vid = ""
    if "v=" in url:
        vid = url.split("v=")[1].split("&")[0]
    thumb = f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg" if vid else ""

    return layout("YouTube Thumbnail Downloader", f"""
    <form>
        <input class="form-control mb-3" name="url" placeholder="YouTube URL">
        <button class="btn btn-dark">Get Thumbnail</button>
    </form>
    {"<img src='"+thumb+"' width='400'>" if thumb else ""}
    """)

# API
@app.route("/api")
def api():
    return {"status": "ok"}