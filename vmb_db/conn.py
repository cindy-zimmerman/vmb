import datetime
import MySQLdb
from MySQLdb.cursors import SSDictCursor
from conf import getModule
config = getModule('mysqlConfig')
mysql = config.main



def get_db(db=None):
    try:
        if db is None:
            db = MySQLdb.connect(host=mysql['host'], # your host, usually localhost
                             user=mysql['user'], # your username
                              passwd=mysql['password'], # your password
                              db=str(mysql['database'])) # name of the data base
                            # cursorclass = SSDictCursor)

        cursor = db.cursor()
        try:
            cursor.execute("SELECT VERSION()")
            results = cursor.fetchone()
            ver = results[0]
        except:
            print "ERROR IN CONNECTION"
            return False

        return db
    except MySQLdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])

def error_mess(pythonFile, function, errorMess):
    now = datetime.datetime.now().isoformat()

    query = "INSERT INTO VMB.error_messages(\
        file_name, function, message, error_date) " \
        "VALUES(%s,%s,%s,%s)"
    args = (pythonFile, function, errorMess[:100], now)

    db = get_db()
    cur = db.cursor()

    cur.execute(query, args)
    db.commit()

    cur.close()
    db.close()

def iterate_query(query, connection=None, arraysize=1):
    # https://gist.github.com/robcowie/814599
    if connection is None:
        connection = get_db(None)
    c = connection.cursor(cursorclass=SSDictCursor)
    c.execute(query)
    while True:
        nextrows = c.fetchmany(arraysize)
        if not nextrows:
            break
        for row in nextrows:
            yield row
    c.close()

def get_one(query, connection=None):
    if connection is None:
        connection = get_db(None)
    cur = connection.cursor(cursorclass=SSDictCursor)
    cur.execute(query)
    results = cur.fetchoneDict()
    cur.close()
    return results