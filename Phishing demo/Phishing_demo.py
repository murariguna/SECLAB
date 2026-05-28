import logging
import threading
import time
import webbrowser
from datetime import datetime

from flask import Flask, render_template, render_template_string, request

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("phishing_demo")

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    received = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Console only — nothing is stored or transmitted
    sep = "─" * 44
    logger.info(sep)
    logger.info("  PHISHING AWARENESS DEMO  ·  credential capture")
    logger.info(sep)
    logger.info("  Timestamp : %s", received)
    logger.info("  Email     : %s", email    or "(empty)")
    logger.info("  Password  : %s", password or "(empty)")
    logger.info(sep)

    return render_template_string(RESPONSE_PAGE)


RESPONSE_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Awareness Demo Complete</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'DM Sans', sans-serif;
            background: #0d1117;
            overflow: hidden;
            position: relative;
        }

        .glow {
            position: fixed;
            border-radius: 50%;
            pointer-events: none;
        }
        .glow-1 {
            width: 420px; height: 420px;
            background: radial-gradient(circle, rgba(34,197,94,0.14) 0%, transparent 70%);
            top: -120px; left: -80px;
            animation: drift 10s ease-in-out infinite alternate;
        }
        .glow-2 {
            width: 380px; height: 380px;
            background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
            bottom: -100px; right: -60px;
            animation: drift 10s ease-in-out infinite alternate-reverse;
        }
        @keyframes drift {
            from { transform: translate(0, 0); }
            to   { transform: translate(30px, 40px); }
        }

        .card {
            position: relative;
            z-index: 10;
            width: 500px;
            padding: 52px 48px;
            border-radius: 20px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.11);
            backdrop-filter: blur(24px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.55);
            animation: fadeUp 0.55s cubic-bezier(0.22,1,0.36,1) both;
            text-align: center;
        }
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(20px) scale(0.97); }
            to   { opacity: 1; transform: translateY(0) scale(1); }
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: rgba(34,197,94,0.12);
            border: 1px solid rgba(34,197,94,0.25);
            border-radius: 100px;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 500;
            color: #4ade80;
            letter-spacing: 0.3px;
            margin-bottom: 28px;
        }
        .badge-dot {
            width: 7px; height: 7px;
            border-radius: 50%;
            background: #4ade80;
        }

        .icon-wrap {
            width: 64px; height: 64px;
            border-radius: 16px;
            background: rgba(34,197,94,0.1);
            border: 1px solid rgba(34,197,94,0.2);
            display: flex; align-items: center; justify-content: center;
            font-size: 28px;
            margin: 0 auto 24px;
        }

        h1 {
            font-size: 22px;
            font-weight: 600;
            color: #f1f5f9;
            letter-spacing: -0.3px;
            margin-bottom: 14px;
        }

        p {
            font-size: 15px;
            line-height: 1.75;
            color: #94a3b8;
        }

        .divider {
            height: 1px;
            background: rgba(255,255,255,0.09);
            margin: 28px 0;
        }

        .tip-label {
            font-size: 11px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #475569;
            margin-bottom: 10px;
        }

        .tip-text {
            font-size: 14px;
            line-height: 1.7;
            color: #64748b;
        }

        .btn {
            display: inline-block;
            margin-top: 28px;
            padding: 12px 28px;
            font-family: 'DM Sans', sans-serif;
            font-size: 14px;
            font-weight: 600;
            color: #fff;
            background: linear-gradient(135deg, #166534, #15803d);
            border: none;
            border-radius: 10px;
            cursor: pointer;
            text-decoration: none;
            transition: opacity 0.2s, transform 0.15s;
        }
        .btn:hover { opacity: 0.88; transform: translateY(-1px); }
    </style>
</head>
<body>

    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>

    <div class="card">
        <div class="badge">
            <div class="badge-dot"></div>
            Simulation complete
        </div>

        <div class="icon-wrap">&#x2705;</div>

        <h1>You completed the demo</h1>

        <p>
            This was a <strong style="color:#f1f5f9;font-weight:500">safe, local
            phishing-awareness simulation</strong>. No data was sent anywhere —
            your credentials were only printed to the terminal running this server.
        </p>

        <div class="divider"></div>

        <div class="tip-label">Why this matters</div>
        <p class="tip-text">
            Real phishing pages look exactly like this one. Always check the URL
            in your browser's address bar before entering any credentials.
        </p>

        <a href="/" class="btn">&#8592; Back to login demo</a>
    </div>

</body>
</html>
"""

def _open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    logger.info("─" * 44)
    logger.info("  Phishing Awareness Demo")
    logger.info("  http://127.0.0.1:5000")
    logger.info("─" * 44)

    threading.Thread(target=_open_browser, daemon=True).start()
    app.run(debug=False)