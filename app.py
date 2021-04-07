import bson
import json
from bson import ObjectId
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_pymongo import PyMongo
from passlib.hash import pbkdf2_sha256 as encryptor

from db import MongoDBConnector

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
    output = bdd.get_all_citations()
    for elem in output:
        elem['_id'] = str(elem['_id'])

    return render_template(page_index, list_citations=output)


def tranform_list(list_to_transform):
    for elem in list_to_transform:
        elem['_id'] = str(elem['_id'])
    return list_to_transform





@app.route('/connexion/', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        login_user = bdd.get_user(request.form['mail'])

        if login_user:
            if encryptor.verify(request.form['password'], login_user['pwd']):
                session['mail'] = request.form['mail']
                session['favorite'] = login_user['favorite']

                return redirect('/')
            return 'Email ou mot de passe incorrect(s)'
    return render_template('auth/connexion.html')


@app.route('/deconnexion/')
def deconnexion():
    session.pop('mail', None)
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

        test2 = bdd.get_citation_by_text(input_citation)
        if input_citation != "" and test2 is None:
            bdd.add_citation(input_citation, input_author, input_oeuvre, input_date, input_langue, session['mail'])

            cit = bdd.get_citation_by_text(input_citation)
            bdd.user_add_mes_ajouts(session['mail'], cit['_id'])

            print("Vous avez bien ajouté la citation")

    return redirect('/')


@app.route('/', methods=['POST'])
def research_citation2():
    input_mode = request.form['mode_recherche']
    input_research = request.form['recherche']
    all_citations = mongo.db.citation
    output = []
    if input_mode == "0":
        for c in all_citations.find():
            y = c['text'].find(input_research)
            if y != -1:
                output.append(c)
        return render_template(page_index, list_citations=tranform_list(output))
    elif input_mode == "1":
        for c in all_citations.find():
            if "author" in c:
                y = c['author'].find(input_research)
                if y != -1:
                    output.append(c)
        return render_template(page_index, list_citations=tranform_list(output))
    elif input_mode == "2":
        for c in all_citations.find():
            y = c['text'].find(input_research)
            if y != -1:
                output.append(c)
        return render_template(page_index, list_citations=tranform_list(output))
    elif input_mode == "3":
        user = bdd.get_user(session['mail'])
        list_citations_favorite = []
        output2 = []
        for id_cit in user['favorite']:
            citation = bdd.get_citation(ObjectId(id_cit))
            list_citations_favorite.append(citation)
        if input_research is not None and input_research != "":
            for c in list_citations_favorite:
                y = c['text'].find(input_research)
                if y != -1:
                    output.append(c)
            for c in list_citations_favorite:
                y = c['author'].find(input_research)
                if y != -1:
                    output2.append(c)
            if len(output) < len(output2):
                return render_template(page_index, list_citations=tranform_list(output2))
            else:
                return render_template(page_index, list_citations=tranform_list(output))
        else:

            for elem in list_citations_favorite:
                if elem:
                    output.append(elem)
            return render_template(page_index, list_citations=tranform_list(output))
    elif input_mode == "4":
        user = bdd.get_user(session['mail'])
        list_citations_favorite = []
        output2 = []
        for id_cit in user['mes_ajouts']:
            citation = bdd.get_citation(ObjectId(id_cit))
            list_citations_favorite.append(citation)
        for c in list_citations_favorite:
            y = c['text'].find(input_research)
            if y != -1:
                output.append(c)
        for c in list_citations_favorite:
            y = c['author'].find(input_research)
            if y != -1:
                output2.append(c)
        if len(output) < len(output2):
            return render_template(page_index, list_citations=tranform_list(output2))
        else:
            return render_template(page_index, list_citations=tranform_list(output))
    elif input_mode == "5":
        output3 = bdd.get_sorted_citation()
        for c in output3:
            output.append(bdd.get_citation(ObjectId(c['_id'])))
        return render_template(page_index, list_citations=tranform_list(output))
    else:
        return render_template(page_index, list_citations=bdd.get_all_citations())


@app.route('/button', methods=['POST'])
def onclick_delete_citation():
    id_citation = request.form['delete']
    bdd.user_remove_mes_ajouts(session['mail'], ObjectId(id_citation))
    bdd.delete_citation(ObjectId(id_citation))
    if ObjectId(id_citation) in session['favorite']:
        bdd.user_remove_favorite(session['mail'], ObjectId(id_citation))
    return redirect('/')


@app.route('/favorite', methods=['POST'])
def add_or_rm_favorite():
    user = bdd.get_user(session['mail'])
    favorite = user['favorite']
    id_citation = request.form['fav']

    if id_citation in favorite:
        bdd.user_remove_favorite(session['mail'], id_citation)
    else:
        bdd.user_add_favorite(session['mail'], id_citation)
    session['favorite'] = bdd.get_user(session['mail'])['favorite']
    return redirect('/')


@app.route('/stats', methods=['GET'])
def stats():
    bestauthor = str(bdd.best_author()[1]['_id'])
    bestuser = str(bdd.best_user()[0]['id'])
    print(bestauthor)
    citations = bdd.get_all_citations()
    count = 0
    top3_citations = bdd.get_sorted_citation()
    output = []
    premier_auteur = True

    for citation in top3_citations:
        print(citation)
        if premier_auteur:
            premier_auteur = False
            auteur_fav = bdd.get_citation(citation['_id'])['author']
        citation_entiere = bdd.get_citation(citation['_id'])
        citation_entiere["count"] = citation["sum"]
        output.append(citation_entiere)
    for elem in citations:
        if not elem['author']:
            count += 1
    return render_template('stats.html', meilleur_auteur=bestauthor, meilleur_user=bestuser, citation_sans_auteur=count,
                           best_citations=output, auteur_le_plus_fav = auteur_fav, top3stats= top3_citations)


if __name__ == "__main__":
    app.run(debug=True)
