from flask import Flask, render_template_string


app = Flask(__name__)


HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Israel Analog Clock</title>
  <style>
    html, body {
      height: 100%;
      margin: 0;
    }
    body {
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      display: grid;
      place-items: center;
      background: #f7f7f7;
    }
    .clock-wrap {
      width: 320px;
      height: 320px;
      border: 8px solid #222;
      border-radius: 50%;
      background: #fff;
      position: relative;
      box-shadow: 0 6px 18px rgba(0,0,0,.15);
    }
    /* tick marks */
    .tick {
      position: absolute;
      left: 50%;
      top: 50%;
      width: 2px;
      height: 140px;
      background: transparent;
      transform-origin: bottom center;
    }
    .tick:after {
      content: "";
      position: absolute;
      left: -1px;
      top: 0;
      width: 4px;
      height: 14px;
      background: #222;
      border-radius: 2px;
    }
    /* hour ticks thicker */
    .tick.hr:after {
      height: 18px;
      width: 5px;
      left: -1.5px;
      background: #000;
    }
    /* hands */
    .hand {
      position: absolute;
      left: 50%;
      top: 50%;
      transform-origin: bottom center;
      transform: translate(-50%, -100%) rotate(0deg);
      border-radius: 6px;
    }
    .hand.hour {
      width: 8px;
      height: 85px;
      background: #000;
    }
    .hand.min {
      width: 6px;
      height: 110px;
      background: #333;
    }
    .hand.sec {
      width: 2px;
      height: 130px;
      background: #e11;
    }
    /* center cap */
    .cap {
      position: absolute;
      left: 50%;
      top: 50%;
      width: 14px;
      height: 14px;
      background: #000;
      border-radius: 50%;
      transform: translate(-50%, -50%);
      z-index: 3;
    }
    /* date in the middle */
    .date {
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      font-size: 14px;
      color: #111;
      text-align: center;
      line-height: 1.2;
      width: 120px;
      z-index: 2;
      pointer-events: none;
    }
    .label {
      margin-top: 4px;
      font-size: 12px;
      color: #666;
    }
  </style>
</head>
<body>
  <div class="clock-wrap" id="clock">
    <!-- 12 major ticks and 48 minor ticks -->
  </div>

  <script>
    (function () {
      const tz = "Asia/Jerusalem";

      const root = document.getElementById("clock");

      // build ticks
      for (let i = 0; i < 60; i++) {
        const t = document.createElement("div");
        t.className = "tick" + (i % 5 === 0 ? " hr" : "");
        t.style.transform =
          "translate(-50%, -100%) rotate(" + (i * 6) + "deg)";
        root.appendChild(t);
      }

      // hands
      const hour = document.createElement("div");
      hour.className = "hand hour";
      const min = document.createElement("div");
      min.className = "hand min";
      const sec = document.createElement("div");
      sec.className = "hand sec";

      // date
      const dateEl = document.createElement("div");
      dateEl.className = "date";

      // center cap
      const cap = document.createElement("div");
      cap.className = "cap";

      root.appendChild(hour);
      root.appendChild(min);
      root.appendChild(sec);
      root.appendChild(dateEl);
      root.appendChild(cap);

      const fmt = new Intl.DateTimeFormat(
        "en-GB",
        {
          timeZone: tz,
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
          weekday: "short",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
          hour12: false
        }
      );

      function partsFor(date) {
        const parts = fmt.formatToParts(date);
        const get = k => parts.find(p => p.type === k).value;
        return {
          y: parseInt(get("year"), 10),
          m: parseInt(get("month"), 10),
          d: parseInt(get("day"), 10),
          wd: get("weekday"),
          hh: parseInt(get("hour"), 10),
          mm: parseInt(get("minute"), 10),
          ss: parseInt(get("second"), 10)
        };
      }

      function update() {
        const now = new Date();
        const p = partsFor(now);

        const h = p.hh % 12;
        const m = p.mm;
        const s = p.ss;

        const hDeg = (h * 30) + (m * 0.5) + (s * (0.5 / 60));
        const mDeg = (m * 6) + (s * 0.1);
        const sDeg = s * 6;

        hour.style.transform =
          "translate(-50%, -100%) rotate(" + hDeg + "deg)";
        min.style.transform =
          "translate(-50%, -100%) rotate(" + mDeg + "deg)";
        sec.style.transform =
          "translate(-50%, -100%) rotate(" + sDeg + "deg)";

        dateEl.innerHTML =
          p.wd + "<br>" +
          String(p.d).padStart(2, "0") + " / " +
          String(p.m).padStart(2, "0") + " / " +
          p.y + '<div class="label">Israel Time</div>';
      }

      update();
      setInterval(update, 1000);
    })();
  </script>
</body>
</html>
"""


@app.route("/")
def index():
  # Pure client-side TZ handling; server stays simple.
  return render_template_string(HTML)


if __name__ == "__main__":
    app.run(debug=True)
