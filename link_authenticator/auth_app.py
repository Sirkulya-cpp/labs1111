from flask import Flask, render_template, request, redirect
from flask_cors import CORS

import auth_authentication

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def home():
    return render_template('index.html', template_folder="templates")


@app.route('/api/login', methods=['POST'])
def user_input():
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


def login(user_login, user_password):
    if auth_authentication.try_user_login(user_login, user_password):
        return redirect(url_for('link_shortener', _external=True) + 'successful_auth')
    else:
        return "Wrong login or password, please try again"


def signup(user_login, user_password):
    if auth_authentication.try_user_signup(user_login, user_password):
        #return redirect(url_for('link_shortener', _external=True) + 'successful_auth')
        return redirect('/link_shortener/successful_auth')
    else:
        return "Wrong login or password, please try again"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
