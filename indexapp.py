
from flask import Flask, render_template, url_for , make_response
from flask import request, redirect
from flask_bootstrap import Bootstrap


app = Flask(__name__, template_folder='front-end/',
            static_folder='front-end/css')
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True, port=5080)
