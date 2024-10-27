from flask import render_template

def home():
    web_name: str = 'Home'
    return render_template('index.html', web_name=web_name)
def padres():
    web_name: str = 'Registro de Padres'
    return render_template('padres.html', web_name=web_name)

