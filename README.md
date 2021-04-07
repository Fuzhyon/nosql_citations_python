# nosql_citations_python

## Participants du Projet

Ce projet à été élaboré par Jeffrey Fevre et Chris Domingues.

### Jeu de Données de test

Après avoir cloné le projet.

Un jeu de données de test est fourni pour le projet.

Ce jeu de données est notre base "Citations_db" qui contient deux collections (citations et user).

Sur Windows: 

Les fichiers se situent dans le dossier db_mongo.

Pour installer cette base de données il faut lancer mongod.exe en arrière plan, extraire l'archive citations_db, se situer dans le dossier d'extraction
et lancer une invite de commandes dans ce même dossier.

Une fois sur l'invite de commande :
Il faut écrire (en ayant mongo dans le path de windows) :

``` bash
mongorestore -d citations_db citations_db
```

Une fois ceci effectué, la base de données sera installé sur votre mongod.

### Installation du Python et de ses librairies

Avoir Python 3.8 ou supérieur installé sur son ordinateur est nécéssaire, et celui-ci doit être présent dans le path de windows.
Voici un lien d'installation : https://www.python.org/downloads/windows/

Une fois python installé sur votre machine, il faut créer un environnement de travail en python.
Pour cela, il faut ouvrir une invite de commande dans le dossier du projet (la ou se situe le requirements.txt)

Puis rentrer les commandes suivantes :

```bash
python -m venv citation_env
```
puis

```bash
citation_env\\Scripts\\activate.bat
```

Sur la gauche, vous verrez (citation_env) entre paranthèse dans votre invite de commande.

Il faut maintenant installer toutes les librairies utilisées dans le projet.

Pour cela, éxécutez la commande suivante :

```bash
pip install -r requirements.txt
```

Une fois ceci installé, vous pourrez lancer le programme.


## Lancer le programme

Pour lancer le programme, rien de plus simple ;) 

Vérifiez que mongod.exe tourne en arrière plan, que la base de données à bien été installée comme indiqué précédemment
et lancez la commande suivante dans votre interface de commandes toujours à la racine du projet (la ou se situe app.py):

```bash
python app.py
```

Ensuite, rendez-vous sur votre navigateur préféré sur l'adresse http://127.0.0.1:5000/

Voila ! Vous pouvez manipuler notre projet de citations.

### Point supplémentaire

Afin d'exploiter certaines fonctionnalités du site, il est nécéssaire de se créer un compte utilisateur, et de se connecter par la suite.

Les mots de passes pour les autres comptes utilisateurs dans notre jeu de données de test sont tous : 01234

### Mot de la fin

Merci pour ce TP qui nous à permis de découvrir le NoSQL avec MongoDB, et le framework Flask en python que nous tennions à essayer,
ce projet à été l'occasion de tester les diverses fonctionnalités de ce dernier.

Cordialement, 

Jeffrey et Chris.
