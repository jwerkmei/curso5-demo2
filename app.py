from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/hola')
def hola():
    return "Hola World!"

@app.route('/bye')
def bye():
    return "Goodbye!"

@app.route('/iniciar-sesion')
def iniciar_sesion():
    return "Iniciar Sesión"

@app.route('/users/<username>')
def users(username):
    return f"Perfil de usuario {username}"