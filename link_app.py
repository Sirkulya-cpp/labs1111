import validators

from flask import Flask, jsonify, redirect, render_template, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)


cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# вхід на сервіс
@app.route("/")
def unauth():
    return render_template("index.html", template_folder="templates")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

