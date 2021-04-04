
from flask import Flask, render_template, Response, request, redirect, url_for
from flask_wtf import form

app = Flask(__name__)


def connexion():
    if request.method == 'POST':
        if request.form['Connexion'] == 'Do Something':
            pass # do something
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('connecter.html', form=form)
def Inscription():
    if request.method == 'POST':
        if request.form['Inscription'] == 'Do Something':
            pass # do something
        elif request.form['Inscription'] == 'Do Something Else':
            pass # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('inscription.html', form=form)