from flask import Flask, render_template_string
from datetime import datetime


app = Flask(__name__)


@app.route("/")
def index():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string("""
<!doctype html>
<html>
<head>
  <meta http-equiv="refresh" content="1">
  <title>Current Clock</title>
  <style>
    body {
      font-family: system-ui, sans-serif;
      display: grid;
      place-items: center;
      height: 100vh;
      margin: 0;
    }
    .clock { font-size: 3rem; }
  </style>
</head>
<body>
  <div class="clock">{{ now }}</div>
</body>
</html>
""", now=now)


if __name__ == "__main__":
    app.run(debug=True)
