from flask import Flask, render_template, request
from db import MongoDBConnector
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'citations_db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/citations_db'
page_index = 'index.html'
mongo = PyMongo(app)
bdd = MongoDBConnector()


# Flask
@app.route('/')
def index_page():
    return render_template(page_index, list_citations=bdd.get_all_citations())


@app.route('/user_list/')
def user_list():
    return render_template('user_list.html', list_users=bdd.get_all_user())


@app.route('/connexion/')
def connexion():
    return render_template('auth/connexion.html')


@app.route('/inscription/')
def inscription_page():
    return render_template('auth/inscription.html')


@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/inscription/', methods=['POST'])
def add_user():
    mail = request.form['email']
    password = request.form['password']
    confirmation_pwd = request.form['confirmPassword']
    if password == confirmation_pwd:
        bdd.add_user(mail, password)
    return render_template(page_index, list_citations=bdd.get_all_citations())


@app.route('/add_citation/')
def launch_citation():
    return render_template('add_citation.html')


@app.route('/add_citation/', methods=['GET', 'POST'])
def add_citation():
    print("coucou")
    return render_template(page_index, list_citations=bdd.get_all_citations())


@app.route('/', methods=['GET', 'POST'])
def research_citation():
    input_auteur = request.form['auteur']
    input_citation = request.form['citation']
    aucune_recherche = input_citation == "" and input_auteur == ""
    citations = mongo.db.citation
    output = []
    if not aucune_recherche:
        for c in citations.find():
            print(c)
            if "author" in c:
                x = c['author'].find(input_auteur)
                y = c['text'].find(input_citation)
                if x != -1 and input_citation == "":
                    output.append({'text': c['text'], 'author': c['author']})
                if y != -1 and input_auteur == "":
                    output.append({'text': c['text'], 'author': c['author']})
                if x != -1 and input_citation != "" and input_auteur != "":
                    output.append({'text': c['text'], 'author': c['author']})
                if y != -1 and input_auteur != "" and input_citation != "":
                    output.append({'text': c['text'], 'author': c['author']})
            elif "author" not in c and input_citation != "":
                print("coucou")
                y = c['text'].find(input_citation)
                if y != -1:
                    output.append({'text': c['text']})
        print(output)
        return render_template(page_index, list_citations=output)
    elif aucune_recherche:
        return render_template(page_index, list_citations=bdd.get_all_citations())


if __name__ == "__main__":
    app.run(debug=True)
