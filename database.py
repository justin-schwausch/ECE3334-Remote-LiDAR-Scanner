import sqlite3  # built for sqlite3


class Database(object):  # database object

    def fetch(self, rbegin, rend, abegin, aend, dbegin, dend):  # fetches specified rows from database
        print(rbegin, rend, abegin, aend, dbegin, dend)
        conn = sqlite3.connect('database.db')  # connect to database
        c = conn.cursor()  # database cursor
        c.execute('SELECT * FROM readings WHERE rowid BETWEEN {0} AND {1} AND angle BETWEEN {2} AND {3} AND distance between {4} AND {5}'.format(rbegin, rend, abegin, aend, dbegin, dend))  # select rows
        results = c.fetchall()  # fetch rows
        conn.close()  # close connection
        return results

    def store(self, readings):  # when given a list of tuples, store them all to the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.executemany('INSERT INTO readings VALUES (?, ?)', readings)  # store values
        conn.commit()  # commit changes

        c.execute('SELECT count(rowid) FROM readings')  # select rows to determine size
        count = c.fetchone()  # fetch row count
        count = int(count[0])  # convert to int
        conn.commit()
        conn.close()
        return count

    def count(self):  # returns the number of rows in the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT count(rowid) FROM readings')  # select rows in database
        count = c.fetchone()
        count = int(count[0])
        conn.commit()
        conn.close()
        return count

    def remove(self, start, end):  # remove specified rows from the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('DELETE FROM readings WHERE rowid BETWEEN {0} AND {1}'.format(start, end))  # delete rows
        conn.commit()

        c.execute('SELECT count(rowid) FROM readings')  # get new row count
        count = c.fetchone()
        count = int(count[0])
        conn.commit()
        conn.close()
        return count

    def fetchall(self):  # returns all rows in database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM readings')
        results = c.fetchall()
        conn.commit()
        conn.close()
        return results
