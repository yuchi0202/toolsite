from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>My Tool Site</h1>
    <ul>
        <li><a href="/qr">QR Code Generator</a></li>
        <li><a href="/password">Password Generator</a></li>
    </ul>
    """

@app.route("/qr")
def qr():
    text = request.args.get("text", "")
    return f"""
    <h1>QR Code Generator</h1>
    <form>
        <input name="text" placeholder="Enter text">
        <button type="submit">Generate</button>
    </form>
    <br>
    <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={text}">
    <br><a href="/">Home</a>
    """

@app.route("/password")
def password():
    import random, string
    pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
    return f"""
    <h1>Password Generator</h1>
    <p>{pwd}</p>
    <a href="/password">Generate New</a>
    <br><a href="/">Home</a>
    """
    
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

@app.route("/api")
def api():
    return {"status": "ok"}
    
