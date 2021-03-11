from flask import Flask, render_template
from db import mongo_access as ma

app = Flask(__name__)


# Flask
@app.route('/')
def index_page():
    return render_template('index.html',list_citations=ma.get_all_citations(ma.get_db()))

@app.route('/user_list')
def hello(name=None):
    return render_template('user_list.html',list_users=ma.get_all_user(ma.get_db()))

@app.route('/connexion')
def connexion():
    return render_template('connecter.html')

@app.route('/inscription')
def inscription():
    return render_template('inscription.html')


if __name__ == "__main__":
    app.run(debug=True)
