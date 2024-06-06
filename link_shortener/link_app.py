import validators

from flask import Flask, jsonify, redirect, render_template, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import link_shortener

app = Flask(__name__)

auth_limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5 per minute"],
    # зберігання в пам'яті для кожного окремого додатку
    storage_uri="memory://",
)

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


# перевірка посилання на валідність
def is_valid_link(url):
    return validators.url(url)


def is_special_ip(ip):
    print(ip)
    return True  # Замініть це на свою умову


# вхід на сервіс
@app.route("/")
@auth_limiter.limit("1/minute", override_defaults=False)
def unauth():
    return redirect("http://link_authenticator")


# авторизація з першого клієнта
@app.route("/successful_auth_1")
@auth_limiter.limit("1/minute", override_defaults=True)
def home_1():
    return render_template("index.html", template_folder="templates")


# авторизація з другого клієнта
@app.route("/successful_auth_2")
@auth_limiter.limit("10/minute", override_defaults=True)
def home_2():
    return render_template("index.html", template_folder="templates")


# редірект по скороченому раніше посиланню
@app.route("/<param>")
def activate_function(param):
    try:
        link = link_shortener.link_lengthen_request(param)
        return redirect(link)
    except Exception as e:
        print(e)
        return "incorrect link"


# скорочення лінки
@app.route("/api/shorten_url", methods=["POST"])
def process_data():
    data = request.get_json()
    long_url = data.get("long_url")
    if is_valid_link(long_url):
        result = {
            "message": "http://localhost/link_shortener/"
            + link_shortener.link_shorten_request(str(long_url)),
            "data": data,
        }
    else:
        result = {
            "message": "Incorrect link. Please try the correct one.",
            "data": data,
        }

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    a = 1 + "jopa"
