from flask import Flask, request
import random, string

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

                <div class="col-md-4">
                    <div class="card shadow-sm mb-4">
                        <div class="card-body">
                            <h5 class="card-title">QR Code Generator</h5>
                            <p class="card-text">QR Code 產生器</p>
                            <a href="/qr" class="btn btn-primary">Open 開啟</a>
                        </div>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="card shadow-sm mb-4">
                        <div class="card-body">
                            <h5 class="card-title">Password Generator</h5>
                            <p class="card-text">密碼產生器</p>
                            <a href="/password" class="btn btn-success">Open 開啟</a>
                        </div>
                    </div>
                </div>

            </div>

            <footer class="text-center mt-5 text-muted">
                My Tool Site © 2026
            </footer>
        </div>
    </body>
    </html>
    """

# QR Code
@app.route("/qr")
def qr():
    text = request.args.get("text", "")
    return f"""
    <html>
    <head>
        <title>QR Code Generator</title>
        {BOOTSTRAP}
    </head>
    <body class="bg-light">
        <div class="container py-5">
            <h1 class="mb-4">QR Code Generator QR Code 產生器</h1>

            <form>
                <input class="form-control mb-3" name="text" placeholder="Enter text / 輸入文字">
                <button class="btn btn-primary">Generate 產生</button>
            </form>

            <div class="mt-4">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={text}">
            </div>

            <br>
            <a href="/" class="btn btn-secondary">Home 首頁</a>
        </div>
    </body>
    </html>
    """

# Password
@app.route("/password")
def password():
    pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
    return f"""
    <html>
    <head>
        <title>Password Generator</title>
        {BOOTSTRAP}
    </head>
    <body class="bg-light">
        <div class="container py-5">
            <h1 class="mb-4">Password Generator 密碼產生器</h1>

            <div class="card p-4">
                <h3>{pwd}</h3>
                <a href="/password" class="btn btn-success mt-3">Generate New 重新產生</a>
            </div>

            <br>
            <a href="/" class="btn btn-secondary">Home 首頁</a>
        </div>
    </body>
    </html>
    """

# sitemap
@app.route("/sitemap.xml")
def sitemap():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url>
        <loc>https://web-production-c1029.up.railway.app/</loc>
      </url>
      <url>
        <loc>https://web-production-c1029.up.railway.app/qr</loc>
      </url>
      <url>
        <loc>https://web-production-c1029.up.railway.app/password</loc>
      </url>
    </urlset>
    """

# API
@app.route("/api")
def api():
    return {"status": "ok"}