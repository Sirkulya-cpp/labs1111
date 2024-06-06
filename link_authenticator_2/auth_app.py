import time

import redis
from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
#from flask_limiter import Limiter

import auth_authentication

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

redis_conn = redis.Redis(host = 'link_redis_db', port = 6379, db = 0, decode_responses=True)
REDIS_LIMIT = 4


def update_activity(user_ip: str) -> None:
    activity_key = f"activity:{user_ip}"
    timestamp = int(time.time())
    redis_conn.zadd(activity_key, {timestamp: timestamp})
    redis_conn.expire(activity_key, 60)  # Встановлення TTL на 60 секунд (1 хвилина)


# default index page
@app.route('/')
def home() -> str:

    user_ip = str(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr))
    #print("=====", user_ip)
    current_count = int(redis_conn.get(user_ip) or 0)


    if current_count >= REDIS_LIMIT:
        #redis_conn.lpush(user_ip, int(time.time()))  # Додаємо мітку часу для сортування черги
        update_activity(user_ip)
        return jsonify({"message": "Request limit exceeded. Please wait in the queue."}), 429

    redis_conn.incr(user_ip)
    redis_conn.expire(user_ip, 60)
    update_activity(user_ip)
    return render_template('index.html', template_folder = "templates")


# login/signup API
@app.route('/api/login', methods=['POST'])
def user_input() -> str:
    print("JOPA")
    user_login = request.form['login']
    user_password = request.form['password']
    action = request.form['action']

    if action == "login":
        result = login(user_login, user_password)
    elif action == "signup":
        result = signup(user_login, user_password)
    else:
        result = "Wrong API Call"

    return result


# login function
def login(user_login: str, user_password: str) -> str:
    if auth_authentication.try_user_login(user_login, user_password):
        # return redirect(url_for('link_shortener', _external=True) + 'successful_auth')
        return redirect('/link_shortener/successful_auth_2')
    else:
        return "Wrong login or password, please try again"

# signup function
def signup(user_login: str, user_password: str) -> str:
    if auth_authentication.try_user_signup(user_login, user_password):
        # return redirect(url_for('link_shortener', _external=True) + 'successful_auth')
        return redirect('/link_shortener/successful_auth_2')
    else:
        return "Wrong login or password, please try again"

# main app run function
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
