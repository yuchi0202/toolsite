from flask import Flask, request
import random, string, base64, urllib.parse, time, datetime

app = Flask(__name__)

BOOTSTRAP = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
"""

# 首頁
@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <title>My Tool Site</title>
        {BOOTSTRAP}
    </head>
    <body class="bg-light">
        <div class="container py-5">
            <h1 class="text-center mb-4">My Tool Website 工具網站</h1>
            <div class="row">

                {tool_card("QR Code Generator", "QR Code 產生器", "/qr", "primary")}
                {tool_card("Password Generator", "密碼產生器", "/password", "success")}
                {tool_card("Base64 Tool", "Base64 編碼解碼", "/base64tool", "warning")}
                {tool_card("URL Encode Tool", "URL 編碼解碼", "/urltool", "info")}
                {tool_card("Timestamp Tool", "時間戳轉換", "/timestamp", "secondary")}

            </div>
            <footer class="text-center mt-5 text-muted">
                My Tool Site © 2026
            </footer>
        </div>
    </body>
    </html>
    """

def tool_card(title, subtitle, link, color):
    return f"""
    <div class="col-md-4">
        <div class="card shadow-sm mb-4">
            <div class="card-body">
                <h5 class="card-title">{title}</h5>
                <p class="card-text">{subtitle}</p>
                <a href="{link}" class="btn btn-{color}">Open 開啟</a>
            </div>
        </div>
    </div>
    """

# QR Code
@app.route("/qr")
def qr():
    text = request.args.get("text", "")
    return page_template("QR Code Generator QR Code 產生器", f"""
        <form>
            <input class="form-control mb-3" name="text" placeholder="Enter text / 輸入文字">
            <button class="btn btn-primary">Generate 產生</button>
        </form>
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={text}">
    """)

# Password
@app.route("/password")
def password():
    pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
    return page_template("Password Generator 密碼產生器", f"""
        <div class="card p-4">
            <h3>{pwd}</h3>
            <a href="/password" class="btn btn-success mt-3">Generate New 重新產生</a>
        </div>
    """)

# Base64
@app.route("/base64tool")
def base64tool():
    text = request.args.get("text", "")
    encoded = base64.b64encode(text.encode()).decode() if text else ""
    decoded = base64.b64decode(text.encode()).decode(errors="ignore") if text else ""
    return page_template("Base64 Encode Decode Base64 編碼解碼", f"""
        <form>
            <input class="form-control mb-3" name="text" placeholder="Enter text">
            <button class="btn btn-warning">Convert 轉換</button>
        </form>
        <p><b>Encoded:</b> {encoded}</p>
        <p><b>Decoded:</b> {decoded}</p>
    """)

# URL Encode
@app.route("/urltool")
def urltool():
    text = request.args.get("text", "")
    encoded = urllib.parse.quote(text)
    decoded = urllib.parse.unquote(text)
    return page_template("URL Encode Decode URL 編碼解碼", f"""
        <form>
            <input class="form-control mb-3" name="text" placeholder="Enter text">
            <button class="btn btn-info">Convert 轉換</button>
        </form>
        <p><b>Encoded:</b> {encoded}</p>
        <p><b>Decoded:</b> {decoded}</p>
    """)

# Timestamp
@app.route("/timestamp")
def timestamp():
    ts = request.args.get("ts", "")
    now = int(time.time())
    result = ""
    if ts:
        try:
            result = datetime.datetime.fromtimestamp(int(ts))
        except:
            result = "Invalid timestamp"
    return page_template("Timestamp Converter 時間戳轉換", f"""
        <p>Current Timestamp 現在時間戳： <b>{now}</b></p>
        <form>
            <input class="form-control mb-3" name="ts" placeholder="Enter timestamp">
            <button class="btn btn-secondary">Convert 轉換</button>
        </form>
        <p><b>Result:</b> {result}</p>
    """)

def page_template(title, content):
    return f"""
    <html>
    <head>
        <title>{title}</title>
        {BOOTSTRAP}
    </head>
    <body class="bg-light">
        <div class="container py-5">
            <h1 class="mb-4">{title}</h1>
            {content}
            <br>
            <a href="/" class="btn btn-dark">Home 首頁</a>
        </div>
    </body>
    </html>
    """

# sitemap
@app.route("/sitemap.xml")
def sitemap():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url><loc>https://web-production-c1029.up.railway.app/</loc></url>
      <url><loc>https://web-production-c1029.up.railway.app/qr</loc></url>
      <url><loc>https://web-production-c1029.up.railway.app/password</loc></url>
      <url><loc>https://web-production-c1029.up.railway.app/base64tool</loc></url>
      <url><loc>https://web-production-c1029.up.railway.app/urltool</loc></url>
      <url><loc>https://web-production-c1029.up.railway.app/timestamp</loc></url>
    </urlset>
    """

# API
@app.route("/api")
def api():
    return {"status": "ok"}