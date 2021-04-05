from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from db import MongoDBConnector
from flask_pymongo import PyMongo
from passlib.hash import pbkdf2_sha256 as encryptor


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'citations_db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/citations_db'
app.secret_key = b'\xaa\x9a`\x9b\x91\xeb\xeb\xe5O\xbc\xc7\x9c\xa93\x84H'
page_index = 'index.html'
mongo = PyMongo(app)
bdd = MongoDBConnector()


# Flask
@app.route('/')
def index():
    if 'mail' in session:
        print("Connecté avec l'adresse : " + session['mail'])
    else:
        print("Non connecté")
    return render_template(page_index, list_citations=bdd.get_all_citations())


@app.route('/user_list/')
def user_list():
    return render_template('user_list.html', list_users=bdd.get_all_user())


@app.route('/connexion/', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        login_user = bdd.get_user(request.form['mail'])

        if login_user:
            if encryptor.verify(request.form['password'], login_user['pwd']):
                session['mail'] = request.form['mail']
                print(session)
                return redirect(url_for('index'))
            return 'Email ou mot de passe incorrect(s)'
    return render_template('auth/connexion.html')

@app.route('/deconnexion/')
def deconnexion():
    session.pop('mail',None)
    return redirect('/')


@app.route('/inscription/', methods=['POST', 'GET'])
def inscription():
    if request.method == 'POST':
        mail = request.form['email']
        password = request.form['password']
        confirmation_pwd = request.form['confirmPassword']
        if request.form['password'] == confirmation_pwd:
            password = encryptor.encrypt(password)
            if bdd.mail_already_exist(mail):
                return jsonify({"error": "Cette adresse mail existe déjà"}), 400
            bdd.add_user(mail, password)
        return redirect('/')
    return render_template('auth/inscription.html')


@app.route('/add_citation/')
def launch_citation():
    return render_template('add_citation.html')


@app.route('/add_citation/', methods=['POST'])
def add_citation():
    if session['mail']:
        input_citation = request.form['text']
        input_author = request.form['author']
        input_oeuvre = request.form['oeuvre']
        input_date = request.form['year']
        input_langue = request.form['langue']
        if input_citation != "":
            bdd.add_citation(input_citation, input_author, input_oeuvre, input_date, input_langue, session['mail'])
    else:
        flash("Pour être ajouter des citations il faut se connecter")
    return render_template(page_index, list_citations=bdd.get_all_citations())


@app.route('/', methods=['POST'])
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
                y = c['text'].find(input_citation)
                if y != -1:
                    output.append({'text': c['text']})
        return render_template(page_index, list_citations=output)
    elif aucune_recherche:
        return render_template(page_index, list_citations=bdd.get_all_citations())


@app.route('/button', methods=['POST'])
def onclick_delete_citation():
    print("truc et id : "+ request.form['delete'])
    test = bdd.get_citation()

    #print(test)
    return render_template(page_index, list_citations=bdd.get_all_citations())


if __name__ == "__main__":
    app.run(debug=True)
