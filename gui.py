from wrapper import Wrapper  # custom Python LiDAR wrapper
from database import Database  # custom database wrapper
import password # stores passphrase for row removal
import flask  # flask for web hosting
from flask import request  # flask requests
import os  # os for file operations
import plotly.express as px  # plotly express for graphing
import pandas as pd  # pandas to convert to pd dataframe for graphing

port = '/dev/ttyUSB0'  # USB port for LiDAR
password = password.password # passphrase to prevent casual vandalism
db = Database()  # instantiate database
wrapper = Wrapper(port)  # instantiate wrapper

app = flask.Flask(__name__)  # flask app
app.config["DEBUG"] = True  # enable Flask debug for web server


@app.route('/')  # root address
def index():
    count = db.count()  # update database size
    return flask.render_template('ui.html', count=count)  # return ui


@app.route('/static/favicon.ico') # serve favicon
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/start')  # triggers sampling and stores to database
def start():
    secs = int(request.args.get('time', None)) # grab seconds from query
    doreturn = str(request.args.get('return', None)) # should return data
    count = db.store(wrapper.output(secs))  # triggers sampling, stores to database, updates count
    if (doreturn.lower() == 'none'): # if no data should be returned
        return flask.render_template('ui.html', count=count)  # return ui

    else:

       begin = count - (secs * 2000) # start point

    if(doreturn == 'raw'):
        return flask.redirect(flask.url_for('read') + f'?dorow=true&doangle=false&dodist=false&rbegin={begin}&rend={count}') # redirect to raw data
    else: # return graph
        return flask.redirect(flask.url_for('graph') + f'?begin={begin}&end={count}') # redirect to graph



@app.route('/graph')  # graphs rows from db using plotly
def graph():
    if (str(request.args.get('dorow', None)) == 'true'):  # if selecting via rows
        rbegin = str(request.args.get('rbegin', None))  # grab start and end rows
        rend = str(request.args.get('rend', None))

    else:  # else set to default values
        rbegin = '0'  # select from 0 to end of database
        rend = str(db.count())

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

    data = pd.DataFrame(db.fetch(rbegin, rend, abegin, aend, dbegin, dend))  # fetch rows and convert to Pandas dataframe
    frame = px.scatter_polar(data, r=1, theta=0)  # plot data as plotly polar
    spath = os.path.dirname(os.path.realpath('__file__'))  # grab current directory
    path = os.path.join(spath, 'templates/graph.html')  # create path to flask templates folder
    frame.write_html(path)  # save plot to templates folder
    return flask.render_template('graph.html')  # return graph


@app.route('/read')  # return selected rows from db in plaintext
def read():
    if(str(request.args.get('dorow', None)) == 'true'): # if selecting via rows
        rbegin = str(request.args.get('rbegin', None)) # grab start and end rows
        rend = str(request.args.get('rend', None))

    else: # else set to default values
        rbegin = '0' # select from 0 to end of database
        rend = str(db.count())

    if(str(request.args.get('doangle', None)) == 'true'): # if selecting via angle
        abegin = str(request.args.get('abegin', None)) # grab start and end angles
        aend = str(request.args.get('aend', None))

    else: # else set to default values
        abegin = '0' # select from 0 to 360 degrees
        aend = '360'

    if(str(request.args.get('dodist', None)) == 'true'): # if selecting via distance
        dbegin = str(request.args.get('dbegin', None)) # grab start and end distances
        dend = str(request.args.get('dend', None))

    else: # else set to default values
        dbegin = '0' # select from 0 to 12m
        dend = '12000'

    return str(db.fetch(rbegin, rend, abegin, aend, dbegin, dend))  # fetch rows and return them


@app.route('/readall')  # returns all database contents
def readall():
    return str(db.fetchall())


@app.route('/remove')  # remove selected rows from the database
def remove():
    begin = str(request.args.get('begin', None))  # grab beginning and ending rows from GET request
    end = str(request.args.get('end', None))
    pwd = str(request.args.get('pwd', None)) # 'password'
    if (pwd == password):
        count = db.remove(begin, end)  # remove rows and update size
        return flask.render_template('ui.html', count=count, status='Removal Successful')  # return success
    else:
        count = db.count()
        return flask.render_template('ui.html', count=count, status='Incorrect Password')  # return failure


@app.route('/count')  # return size of db in plaintext
def count():
    return str(db.count())


if __name__ == '__main__':  # set up flask service
    app.run(host='0.0.0.0', port=2525)
