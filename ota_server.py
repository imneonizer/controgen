from flask import Flask
import os

app = Flask(__name__)

@app.route("/update")
def update():
    with open("app.py", "rb") as f:
        return f.read()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)