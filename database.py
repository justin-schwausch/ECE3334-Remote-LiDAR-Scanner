'''
A database interface program, designed to store LiDAR readings inside a SQLite3 database on the local system.
Created for CMPE Project Lab, ECE 3334, Summer 2020.

Created by: Justin Schwausch
justinschwausch980@gmail.com

Used in the following Repo: https://github.com/justin-schwausch/ECE3334-Remote-LiDAR-Scanner
This file and the rest of the repo are released under the GNU General Public License v3.0 license.
The code is provided as-is, with no guarantees to functionality or warranties. Users take full responsibility for any
and all damages incurred by using this program or any of this repository.
'''
import sqlite3  # built for sqlite3
from pathlib import Path  # checks for database existence and size


class Database(object):  # database object

    def __init__(self):  # set up database
        print(Path('database.db').is_file())
        if Path('database.db').is_file():  # do nothing if database already exists
            print("Database Exists!")

        else:  # if no database, create one

            print("Database not detected. Creating Database")
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('CREATE TABLE readings(angle real, distance real)')  # one column for angle and one for distance
            conn.commit()
            conn.close()
            print("Database Created")

    def fetch(self, rbegin, rend, abegin, aend, dbegin, dend):  # fetches specified rows from database
        print(rbegin, rend, abegin, aend, dbegin, dend)
        conn = sqlite3.connect('database.db')  # connect to database
        c = conn.cursor()  # database cursor
        c.execute(
            'SELECT * FROM readings WHERE rowid BETWEEN {0} AND {1} AND angle BETWEEN {2} AND {3} AND distance between {4} AND {5}'.format(
                rbegin, rend, abegin, aend, dbegin, dend))  # select rows
        results = c.fetchall()  # fetch rows
        conn.close()  # close connection
        return results

    def store(self, readings):  # when given a list of tuples, store them all to the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.executemany('INSERT INTO readings VALUES (?, ?)', readings)  # store values
        conn.commit()  # commit changes

        c.execute('SELECT count(rowid) FROM readings')  # select rows to determine size
        amount = c.fetchone()  # fetch row count
        amount = int(amount[0])  # convert to int
        conn.commit()
        conn.close()
        size = Path('database.db').stat().st_size / 1000000  # grab physical size of db on disc in MB
        return amount, size

    def count(self):  # returns the number of rows in the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT count(rowid) FROM readings')  # select rows in database
        amount = c.fetchone()
        amount = int(amount[0])
        conn.commit()
        conn.close()
        size = Path('database.db').stat().st_size / 1000000  # grab physical size of db on disc in MB
        return amount, size

    def remove(self, start, end):  # remove specified rows from the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('DELETE FROM readings WHERE rowid BETWEEN {0} AND {1}'.format(start, end))  # delete rows
        conn.commit()
        c.execute('VACUUM')  # delete empty rows
        conn.commit()
        c.execute('SELECT count(rowid) FROM readings')  # get new row count
        amount = c.fetchone()
        amount = int(amount[0])
        conn.commit()
        conn.close()
        size = Path('database.db').stat().st_size / 1000000  # grab physical size of db on disc in MB
        return amount, size

    def fetchall(self):  # returns all rows in database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM readings')
        results = c.fetchall()
        conn.commit()
        conn.close()
        return results
