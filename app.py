from flask import *  # Flask, render_template, request, session
from flask_inputs import Inputs
from flask_pymongo import PyMongo
# from flask.ext.session import Session
import pymongo
import wordFinder

SESSION_TYPE = 'filesystem'

app = Flask(__name__)
app.secret_key = 'secret key lol'

# mongod --auth --dbpath /usr/local/var/mongodb
app.config["MONGO_URI"] = "mongodb://localhost:27017/words"
mongo = PyMongo(app)

collection = mongo.db['combos']

cache = {}

@app.route('/', methods=['GET','POST'])
# @app.route('/index')
def server():

    # global results
    if request.method == 'POST':
        letters = request.form['letters']
        s = ''.join(sorted(letters))
        # res = collection.find_one({'letters': s}, {'_id': 0})  # None type if not found, else a dict
        res = None  # remove
        if res is not None:
            session['w'] = res['words']
        elif s in cache:  # remove
            session['w'] = cache[s]
        else:
            w = wordFinder.words(letters)
            cache[s] = w
            # collection.insert_one({'letters': s, 'words': w})
            session['w'] = w

        return redirect(url_for('results'))  # separate route, or print results on same page?
        # return render_template('index.html', Title='Word Finder', words=w)
    else:
        return render_template('index.html')

@app.route('/results', methods=['GET'])
def results():

    #global results
    return render_template('results.html', words=session['w'])
    #return render_template('results.html', words=results)
    # return 'test'

@app.route('/about')
def about():

    return render_template('about.html')


if __name__ == '__main__':
    app.run()
