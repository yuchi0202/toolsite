from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>My Tool Website</h1>
    <form action="/qr">
        <input name="text" placeholder="Enter text">
        <button type="submit">Generate QR</button>
    </form>
    """

@app.route("/qr")
def qr():
    text = request.args.get("text")
    return f"""
    <h1>QR Code</h1>
    <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={text}">
    <br><a href="/">Back</a>
    """

@app.route("/api")
def api():
    return {"status": "ok"}