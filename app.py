from flask import Flask, render_template
from db import mongo_access as ma
from user.models import User

app = Flask(__name__)

# Flask
@app.route('/')
def index_page():
    return render_template('index.html', list_citations=ma.get_all_citations(ma.get_db()))


@app.route('/user_list/')
def user_list():
    return render_template('user_list.html', list_users=ma.get_all_user(ma.get_db()))


@app.route('/connexion/')
def connexion():
    return render_template('auth/connexion.html')

@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/inscription/')
def inscription():
    return render_template('auth/inscription.html')

@app.route('/user/signup', methods=['GET'])
def signup():
    return User().signup()


if __name__ == "__main__":
    app.run(debug=True)
