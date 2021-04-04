from flask import Flask, render_template ,request
from db import mongo_access as ma
from user.models import User
from flask_pymongo import PyMongo
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'citations_db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/citations_db'
mongo = PyMongo(app)
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

@app.route('/add_citation/')
def launch_citation():
    return render_template('add_citation.html')

@app.route('/add_citation/', methods=['GET','POST'])
def add_citation():
    print("coucou")
    return render_template('index.html', list_citations=ma.get_all_citations(ma.get_db()))


@app.route('/', methods=['GET', 'POST'])
def research_citation():
    inputAuteur = request.form['auteur']
    inputCitation = request.form['citation']
    aucuneRecherche = inputCitation == "" and inputAuteur == ""
    citations = mongo.db.citation
    output = []
    if not aucuneRecherche:
        for c in citations.find():
            print(c)
            if "author" in c:
                x = c['author'].find(inputAuteur)
                y = c['text'].find(inputCitation)
                if x != -1 and inputCitation == "":
                    output.append({'text': c['text'], 'author': c['author']})
                if y != -1 and inputAuteur == "":
                    output.append({'text': c['text'], 'author': c['author']})
                if x != -1 and inputCitation != "" and inputAuteur != "" :
                    output.append({'text': c['text'], 'author': c['author']})
                if y != -1 and inputAuteur != "" and inputCitation != "":
                    output.append({'text': c['text'], 'author': c['author']})
            elif "author" not in c and inputCitation != "":
                print("coucou")
                y = c['text'].find(inputCitation)
                if y != -1:
                    output.append({'text': c['text']})
        print(output)
        return render_template('index.html', list_citations=output)
    elif aucuneRecherche:
        return render_template('index.html',list_citations=ma.get_all_citations(ma.get_db()))



if __name__ == "__main__":
    app.run(debug=True)
