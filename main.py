from flask import Flask, render_template
from db import mongo_access as ma

app = Flask(__name__)


# Flask
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/user_list')
def liste_utilisateurs():
    return render_template('user_list.html', list_users=ma.get_all_user(db))


if __name__ == "__main__":
    db = ma.get_db()
    ma.get_user(db)
    ma.add_user(db)
    truc = (ma.get_all_user(db))
    for elem in truc:
        print(elem)

    app.run(debug=True)
