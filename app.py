from flask import Flask, request
import random, string, base64, urllib.parse, time, datetime, uuid, hashlib, json

app = Flask(__name__)

BOOTSTRAP = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
"""

def layout(title, content):
    return f"""
    <html>
    <head>
        <title>{title}</title>
        <meta name="description" content="{title} Free Online Tool">
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
            {tool_card("Color Picker", "顏色選擇器", "/color", "primary")}
            {tool_card("JSON Formatter", "JSON 格式化", "/json", "success")}
            {tool_card("Text Case", "文字大小寫轉換", "/case", "warning")}
            {tool_card("Word Counter", "字數計算", "/word", "info")}
            {tool_card("Lorem Ipsum", "假文產生器", "/lorem", "secondary")}
            {tool_card("IP Lookup", "IP 查詢", "/ip", "dark")}

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
    <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={text}">
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
    encoded = base64.b64encode(text.encode()).decode() if text else ""
    decoded = ""
    try:
        decoded = base64.b64decode(text.encode()).decode()
    except:
        pass
    return layout("Base64 Tool", f"""
    <form>
        <input class="form-control mb-3" name="text">
        <button class="btn btn-warning">Convert</button>
    </form>
    Encoded: {encoded}<br>
    Decoded: {decoded}
    """)

# URL Encode
@app.route("/urltool")
def urltool():
    text = request.args.get("text", "")
    return layout("URL Encode Decode", f"""
    <form>
        <input class="form-control mb-3" name="text">
        <button class="btn btn-info">Convert</button>
    </form>
    Encoded: {urllib.parse.quote(text)}<br>
    Decoded: {urllib.parse.unquote(text)}
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
    MD5: {md5}<br>
    SHA256: {sha}
    """)

# Color
@app.route("/color")
def color():
    return layout("Color Picker", """
    <input type="color">
    """)

# JSON
@app.route("/json")
def jsontool():
    text = request.args.get("text", "")
    formatted = ""
    try:
        formatted = json.dumps(json.loads(text), indent=4)
    except:
        pass
    return layout("JSON Formatter", f"""
    <form>
        <textarea class="form-control mb-3" name="text" rows="6"></textarea>
        <button class="btn btn-success">Format</button>
    </form>
    <pre>{formatted}</pre>
    """)

# Text case
@app.route("/case")
def casetool():
    text = request.args.get("text", "")
    return layout("Text Case Converter", f"""
    <form>
        <input class="form-control mb-3" name="text">
        <button class="btn btn-warning">Convert</button>
    </form>
    Upper: {text.upper()}<br>
    Lower: {text.lower()}
    """)

# Word Counter
@app.route("/word")
def word():
    text = request.args.get("text", "")
    count = len(text.split())
    return layout("Word Counter", f"""
    <form>
        <textarea class="form-control mb-3" name="text" rows="5"></textarea>
        <button class="btn btn-info">Count</button>
    </form>
    Words: {count}
    """)

# Lorem Ipsum
@app.route("/lorem")
def lorem():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    return layout("Lorem Ipsum Generator", f"""
    <p>{text}</p>
    <a href="/lorem" class="btn btn-secondary">Generate</a>
    """)

# IP
@app.route("/ip")
def ip():
    return layout("IP Lookup", """
    <p>Your IP info:</p>
    <a href="https://api.ipify.org">Check IP</a>
    """)

# API
@app.route("/api")
def api():
    return {"status": "ok"}