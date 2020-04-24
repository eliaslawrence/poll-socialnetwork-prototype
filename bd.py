__author__ = 'Elias'
from google.appengine.ext import db

class Aluno(db.Model):
    nome = db.StringProperty(required = True)
    senha = db.StringProperty(required = True)