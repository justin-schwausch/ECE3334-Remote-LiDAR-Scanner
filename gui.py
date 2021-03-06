'''
This module instantiates the remaining modules and acts as the top of the program.
The module uses Flask to host a web server for users to interact with the program using a web browser.
The module also uses plotly to create interactive polar graphs of LiDAR scan data pulled from a database to be displayed
to the end user.
Created for CMPE Project Lab, ECE 3334, Summer 2020.

Created by: Justin Schwausch
justinschwausch980@gmail.com

Used in the following Repo: https://github.com/justin-schwausch/ECE3334-Remote-LiDAR-Scanner
This file and the rest of the repo are released under the GNU General Public License v3.0 license.
The code is provided as-is, with no guarantees to functionality or warranties. Users take full responsibility for any
and all damages incurred by using this program or any of this repository.
'''
from wrapper import Wrapper  # custom Python LiDAR wrapper
from database import Database  # custom database wrapper
import password  # stores passphrase for row removal
import flask  # flask for web hosting
from flask import request  # flask requests
import os  # os for file operations
import plotly.express as px  # plotly express for graphing
import pandas as pd  # pandas to convert to pd dataframe for graphing

port = '/dev/ttyUSB0'  # USB port for LiDAR
password = password.password  # passphrase to prevent casual vandalism
db = Database()  # instantiate database
wrapper = Wrapper(port)  # instantiate wrapper

app = flask.Flask(__name__)  # flask app
app.config["DEBUG"] = True  # enable Flask debug for web server


@app.route('/')  # root address
def index():
    rows, size = db.count()  # update database size
    print(count)
    return flask.render_template('ui.html', rows=rows, size=size)  # return ui


@app.route('/static/favicon.ico')  # serve favicon
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/start')  # triggers sampling and stores to database
def start():
    amount = int(request.args.get('amount', None))  # grab amount from query
    doreturn = str(request.args.get('return', None))  # should return data
    rows, size = db.store(wrapper.output(amount))  # triggers sampling, stores to database, updates count
    if (doreturn.lower() == 'none'):  # if no data should be returned
        return flask.render_template('ui.html', rows=rows, size=size)  # return ui

    else:

        begin = rows - amount  # start point

    if (doreturn == 'raw'):
        return flask.redirect(flask.url_for(
            'read') + f'?dorow=true&doangle=false&dodist=false&rbegin={begin}&rend={rows}')  # redirect to raw data
    else:  # return graph
        return flask.redirect(flask.url_for('graph') + f'?begin={begin}&end={rows}')  # redirect to graph


@app.route('/graph')  # graphs rows from db using plotly
def graph():
    if (str(request.args.get('dorow', None)) == 'true'):  # if selecting via rows
        rbegin = str(request.args.get('rbegin', None))  # grab start and end rows
        rend = str(request.args.get('rend', None))

    else:  # else set to default values
        rbegin = '0'  # select from 0 to end of database
        rend, stmp = db.count()

    if (str(request.args.get('doangle', None)) == 'true'):  # if selecting via angle
        abegin = str(request.args.get('abegin', None))  # grab start and end angles
        aend = str(request.args.get('aend', None))

    else:  # else set to default values
        abegin = '0'  # select from 0 to 360 degrees
        aend = '360'

    if (str(request.args.get('dodist', None)) == 'true'):  # if selecting via distance
        dbegin = str(request.args.get('dbegin', None))  # grab start and end distances
        dend = str(request.args.get('dend', None))

    else:  # else set to default values
        dbegin = '0'  # select from 0 to 12m
        dend = '12000'

    data = pd.DataFrame(
        db.fetch(rbegin, rend, abegin, aend, dbegin, dend))  # fetch rows and convert to Pandas dataframe
    frame = px.scatter_polar(data, r=1, theta=0)  # plot data as plotly polar
    spath = os.path.dirname(os.path.realpath('__file__'))  # grab current directory
    path = os.path.join(spath, 'templates/graph.html')  # create path to flask templates folder
    frame.write_html(path)  # save plot to templates folder
    return flask.render_template('graph.html')  # return graph


@app.route('/read')  # return selected rows from db in plaintext
def read():
    if (str(request.args.get('dorow', None)) == 'true'):  # if selecting via rows
        rbegin = str(request.args.get('rbegin', None))  # grab start and end rows
        rend = str(request.args.get('rend', None))

    else:  # else set to default values
        rbegin = '0'  # select from 0 to end of database
        rend, atmp = db.count()

    if (str(request.args.get('doangle', None)) == 'true'):  # if selecting via angle
        abegin = str(request.args.get('abegin', None))  # grab start and end angles
        aend = str(request.args.get('aend', None))

    else:  # else set to default values
        abegin = '0'  # select from 0 to 360 degrees
        aend = '360'

    if (str(request.args.get('dodist', None)) == 'true'):  # if selecting via distance
        dbegin = str(request.args.get('dbegin', None))  # grab start and end distances
        dend = str(request.args.get('dend', None))

    else:  # else set to default values
        dbegin = '0'  # select from 0 to 12m
        dend = '12000'

    return str(db.fetch(rbegin, rend, abegin, aend, dbegin, dend))  # fetch rows and return them


@app.route('/readall')  # returns all database contents
def readall():
    return str(db.fetchall())


@app.route('/remove')  # remove selected rows from the database
def remove():
    begin = str(request.args.get('begin', None))  # grab beginning and ending rows from GET request
    end = str(request.args.get('end', None))
    pwd = str(request.args.get('pwd', None))  # 'password'
    if (pwd == password):
        rows, size = db.remove(begin, end)  # remove rows and update size
        return flask.render_template('ui.html', rows=rows, size=size, status='Removal Successful')  # return success
    else:
        rows, size = db.count()
        return flask.render_template('ui.html', rows=rows, size=size, status='Incorrect Password')  # return failure


@app.route('/count')  # return size of db in plaintext
def count():
    return str(db.count())


if __name__ == '__main__':  # set up flask service
    app.run(host='0.0.0.0', port=2525)
