from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Railway!"

@app.route("/api")
def api():
    return {"status": "ok"}
