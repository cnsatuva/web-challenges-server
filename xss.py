#!/usr/bin/env python

from flask import Flask, redirect, render_template, session, request
import os

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('X-XSS-Protection', '0')
    return response

@app.route('/')
def index():
    if 'level' in session:
        return redirect('/level/%s' % session['level'])

    return render_template("xss/index.html")

@app.route('/level')
def levelbasic():
    return redirect("/")

@app.route('/level/<int:level>')
def levelroute(level):

    # Check if the user has a level
    if 'level' not in session:
        session['level'] = 1
        return redirect("/level/1")

    # Check if it's a valid level
    if level not in xrange(1, 5):
        return redirect("/")

    # Has the user unlocked the level?
    if session['level'] < level:
        return redirect("/%s" % session['level'])

    return render_template("xss/level/%s/index.html" % level)

@app.route('/rarecandy/<level>')
def rarecandy(level):
    session['level'] = int(level)
    return redirect("/level/%s" % level)

@app.route('/reset')
def reset():
    try:
        del session['level']
    except:
        pass
    return redirect('/')

@app.route('/advance', methods=['GET'])
def advance():

    if request.headers.get("Referer"):
        current = request.headers.get("Referer")[-1]
        if int(current) in xrange(1, 5):
            try:
                session['level'] = int(current) + 1
                return redirect("/level/%s" % session['level'])
            except:
                pass

    return redirect("/")

# Challenges
@app.route('/submit/1', methods=['POST'])
def submit1():
    try:
        search_term = request.form['search']
    except:
        return redirect("/1")

    return render_template("xss/level/1/search.html", search_term = search_term)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=8080, debug=True)
