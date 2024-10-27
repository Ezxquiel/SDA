from flask import render_template

def home():
    web_name: str = 'Home'
    return render_template('index.html', web_name=web_name)
def parents():
    web_name: str = 'Register parents'
    return render_template('parents.html', web_name=web_name)

