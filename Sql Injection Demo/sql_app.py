import logging
import sqlite3
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
logger = logging.getLogger("sql_demo")

DB_PATH = ":memory:"          # nothing persists; safe for demos
_db_conn: sqlite3.Connection  # module-level connection kept open


def init_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email    TEXT NOT NULL,
            role     TEXT NOT NULL DEFAULT 'user'
        );

        INSERT INTO users (username, email, role) VALUES
            ('alice',  'alice@example.com',  'admin'),
            ('bob',    'bob@example.com',    'user'),
            ('carol',  'carol@example.com',  'user'),
            ('dave',   'dave@example.com',   'moderator'),
            ('eve',    'eve@example.com',    'user');
    """)
    conn.commit()
    return conn

INJECT_KEYWORDS = ("'", "--", ";", "/*", "*/", " or ", " and ", "union",
                   "select", "drop", "insert", "delete", "update")

def looks_like_injection(value: str) -> bool:
    return any(kw in value.lower() for kw in INJECT_KEYWORDS)


def rows_to_list(rows) -> list[dict]:
    return [dict(row) for row in rows]


def _log_query(mode: str, username: str, query: str, row_count: int) -> None:
    sep = "─" * 48
    logger.info(sep)
    logger.info("  SQL INJECTION AWARENESS DEMO  ·  query fired")
    logger.info(sep)
    logger.info("  Mode      : %s", mode)
    logger.info("  Timestamp : %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("  Input     : %s", username or "(empty)")
    logger.info("  Query     : %s", query)
    logger.info("  Rows back : %d", row_count)
    if mode == "VULNERABLE" and looks_like_injection(username):
        logger.warning("  ⚠ Injection payload detected in vulnerable query!")
    logger.info(sep)

RESULT_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Query Result — SQL Demo</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }

        body {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            font-family: 'DM Sans', sans-serif;
            background: #0d1117;
            position: relative;
            overflow-x: hidden;
        }

        .glow { position:fixed; border-radius:50%; pointer-events:none; }
        .glow-1 {
            width:440px; height:440px;
            background: radial-gradient(circle, {{ glow_color }} 0%, transparent 70%);
            top:-140px; left:-100px;
            animation: drift 11s ease-in-out infinite alternate;
        }
        .glow-2 {
            width:380px; height:380px;
            background: radial-gradient(circle, rgba(59,130,246,0.10) 0%, transparent 70%);
            bottom:-100px; right:-70px;
            animation: drift 11s ease-in-out infinite alternate-reverse;
        }
        @keyframes drift {
            from { transform:translate(0,0); }
            to   { transform:translate(35px,45px); }
        }

        .card {
            position: relative;
            z-index: 10;
            width: 100%;
            max-width: 640px;
            padding: 44px 40px;
            border-radius: 20px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.11);
            backdrop-filter: blur(22px);
            box-shadow: 0 20px 56px rgba(0,0,0,0.55);
            animation: fadeUp 0.55s cubic-bezier(0.22,1,0.36,1) both;
        }
        @keyframes fadeUp {
            from { opacity:0; transform:translateY(20px) scale(0.97); }
            to   { opacity:1; transform:translateY(0) scale(1); }
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            border-radius: 100px;
            padding: 5px 13px;
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 0.3px;
            margin-bottom: 24px;
            background: {{ badge_bg }};
            border: 1px solid {{ badge_border }};
            color: {{ badge_color }};
        }
        .badge-dot {
            width:6px; height:6px;
            border-radius:50%;
            background: {{ badge_color }};
        }

        h1 {
            font-size: 21px;
            font-weight: 600;
            color: #f1f5f9;
            letter-spacing: -0.3px;
            margin-bottom: 8px;
        }
        .meta {
            font-size: 13px;
            color: #64748b;
            margin-bottom: 28px;
            line-height: 1.6;
        }

        /* Query block */
        .query-block {
            background: rgba(0,0,0,0.35);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 12px;
            padding: 16px 18px;
            margin-bottom: 24px;
        }
        .query-block p {
            font-size: 11px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.7px;
            color: #475569;
            margin-bottom: 10px;
        }
        .query-block pre {
            font-family: 'DM Mono', monospace;
            font-size: 13px;
            color: #94a3b8;
            white-space: pre-wrap;
            word-break: break-all;
            line-height: 1.7;
        }

        /* Alert banner */
        .alert {
            display: flex;
            gap: 12px;
            align-items: flex-start;
            border-radius: 10px;
            padding: 14px 16px;
            font-size: 13px;
            line-height: 1.65;
            margin-bottom: 24px;
            border: 1px solid;
            background: {{ alert_bg }};
            border-color: {{ alert_border }};
            color: {{ alert_color }};
        }
        .alert-icon { font-size:16px; flex-shrink:0; margin-top:1px; }

        /* Results table */
        .results-label {
            font-size: 11px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.7px;
            color: #475569;
            margin-bottom: 12px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        thead th {
            text-align: left;
            padding: 10px 14px;
            font-size: 11px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: #475569;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        tbody tr {
            border-bottom: 1px solid rgba(255,255,255,0.05);
            transition: background 0.15s;
        }
        tbody tr:hover { background: rgba(255,255,255,0.03); }
        tbody td {
            padding: 11px 14px;
            color: #94a3b8;
            font-family: 'DM Mono', monospace;
        }
        tbody td:first-child { color: #cbd5e1; }

        .role-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 5px;
            font-size: 11px;
            font-family: 'DM Sans', sans-serif;
            font-weight: 500;
        }
        .role-admin { background:rgba(248,113,113,0.12); color:#fca5a5; }
        .role-moderator { background:rgba(245,158,11,0.12); color:#fcd34d; }
        .role-user { background:rgba(96,165,250,0.10); color:#93c5fd; }

        .empty-state {
            text-align: center;
            padding: 32px 0;
            color: #475569;
            font-size: 14px;
        }

        /* Divider */
        .divider { height:1px; background:rgba(255,255,255,0.08); margin:24px 0; }

        .btn {
            display: inline-block;
            padding: 11px 24px;
            font-family: 'DM Sans', sans-serif;
            font-size: 13px;
            font-weight: 600;
            color: #fff;
            background: linear-gradient(135deg, #1e3a5f, #1d4ed8);
            border: none;
            border-radius: 10px;
            cursor: pointer;
            text-decoration: none;
            transition: opacity 0.2s, transform 0.15s;
        }
        .btn:hover { opacity:0.88; transform:translateY(-1px); }
    </style>
</head>
<body>

    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>

    <div class="card">

        <div class="badge">
            <div class="badge-dot"></div>
            {{ badge_label }}
        </div>

        <h1>{{ title }}</h1>
        <p class="meta">
            Input: <code style="font-family:'DM Mono',monospace; color:#e2e8f0;">{{ username }}</code>
            &nbsp;·&nbsp; {{ row_count }} row{{ 's' if row_count != 1 else '' }} returned
        </p>

        <!-- Query used -->
        <div class="query-block">
            <p>Query executed</p>
            <pre>{{ query }}</pre>
        </div>

        <!-- Alert -->
        <div class="alert">
            <span class="alert-icon">{{ alert_icon }}</span>
            <span>{{ alert_message }}</span>
        </div>

        <!-- Result rows -->
        {% if rows %}
            <p class="results-label">Returned rows</p>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Role</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in rows %}
                    <tr>
                        <td>{{ row.id }}</td>
                        <td>{{ row.username }}</td>
                        <td>{{ row.email }}</td>
                        <td>
                            <span class="role-badge role-{{ row.role }}">
                                {{ row.role }}
                            </span>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <div class="empty-state">No matching users found.</div>
        {% endif %}

        <div class="divider"></div>

        <a href="/" class="btn">&#8592; Run another query</a>

    </div>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template("sql_demo.html")


@app.route("/search", methods=["POST"])
def search():
    username = request.form.get("username", "").strip()
    mode     = request.form.get("mode", "vulnerable")  # future toggle
    conn     = _db_conn

    injected = looks_like_injection(username)

    if mode == "safe":
        # ── Parameterised — always safe ──────────────────────────────────────
        query = "SELECT * FROM users WHERE username = ?"
        rows  = rows_to_list(conn.execute(query, (username,)).fetchall())
        _log_query("SAFE", username, f"{query}  [param: {username!r}]", len(rows))

        ctx = dict(
            mode          = "safe",
            username      = username,
            query         = f"SELECT * FROM users WHERE username = ?  -- param: {username!r}",
            rows          = rows,
            row_count     = len(rows),
            title         = "Safe query executed",
            badge_label   = "Parameterised query",
            badge_bg      = "rgba(74,222,128,0.10)",
            badge_border  = "rgba(74,222,128,0.24)",
            badge_color   = "#4ade80",
            glow_color    = "rgba(74,222,128,0.12)",
            alert_bg      = "rgba(74,222,128,0.07)",
            alert_border  = "rgba(74,222,128,0.22)",
            alert_color   = "#86efac",
            alert_icon    = "✅",
            alert_message = (
                "This query used a parameterised statement. "
                "The input is treated as plain data — it cannot alter the SQL structure, "
                "no matter what was typed."
            ),
        )

    else:
        # ── Vulnerable — string concatenation (intentional for demo) ─────────
        query = f"SELECT * FROM users WHERE username = '{username}'"
        try:
            rows = rows_to_list(conn.execute(query).fetchall())
            error = None
        except sqlite3.OperationalError as exc:
            rows  = []
            error = str(exc)

        _log_query("VULNERABLE", username, query, len(rows))

        if error:
            alert_msg = (
                f"The query raised a database error: {error}. "
                "In a real app this stack trace could leak schema details to an attacker."
            )
            alert_icon = "💥"
            alert_bg   = "rgba(248,113,113,0.10)"
            ab         = "rgba(248,113,113,0.24)"
            ac         = "#fca5a5"
        elif injected and len(rows) > 1:
            alert_msg = (
                f"Injection successful — {len(rows)} rows leaked. "
                "The payload broke out of the string literal and rewrote the query logic."
            )
            alert_icon = "⚠️"
            alert_bg   = "rgba(248,113,113,0.10)"
            ab         = "rgba(248,113,113,0.24)"
            ac         = "#fca5a5"
        elif injected:
            alert_msg = (
                "An injection payload was detected in the input. "
                "The query ran as-is — in a real application this could expose or corrupt data."
            )
            alert_icon = "⚠️"
            alert_bg   = "rgba(245,158,11,0.10)"
            ab         = "rgba(245,158,11,0.24)"
            ac         = "#fcd34d"
        else:
            alert_msg = (
                "Normal input — the query returned the expected result. "
                "Now try one of the injection payloads to see what changes."
            )
            alert_icon = "💡"
            alert_bg   = "rgba(255,255,255,0.04)"
            ab         = "rgba(255,255,255,0.08)"
            ac         = "#94a3b8"

        ctx = dict(
            mode          = "vulnerable",
            username      = username,
            query         = query,
            rows          = rows,
            row_count     = len(rows),
            title         = "Vulnerable query executed",
            badge_label   = "String concatenation (unsafe)",
            badge_bg      = "rgba(248,113,113,0.10)",
            badge_border  = "rgba(248,113,113,0.24)",
            badge_color   = "#f87171",
            glow_color    = "rgba(248,113,113,0.10)",
            alert_bg      = alert_bg,
            alert_border  = ab,
            alert_color   = ac,
            alert_icon    = alert_icon,
            alert_message = alert_msg,
        )

    return render_template_string(RESULT_PAGE, **ctx)



def _open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    _db_conn = init_db()

    sep = "─" * 48
    logger.info(sep)
    logger.info("  SQL Injection Awareness Demo")
    logger.info("  http://127.0.0.1:5000")
    logger.info("  In-memory SQLite · no data persists")
    logger.info(sep)

    threading.Thread(target=_open_browser, daemon=True).start()
    app.run(debug=False)