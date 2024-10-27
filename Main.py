from flask import Flask
from router import routers as rt

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_route():
    return rt.home()  # Llama a la función home desde router

@app.route('/parents')
def parents_router():
    return rt.parents()

if __name__ == '__main__':
    app.run(debug=True)
