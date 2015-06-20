__author__ = 'cz'
from vmb_db.conn import get_db, get_one

select = 'SELECT USERS_id, '\
               ' user_name, '\
               ' user_pwd, '\
               ' upload_inv, '\
               ' is_active '\
           ' FROM VMB.USERS '\

def get_user_by_name(user_name=None):

    user_name = user_name.strip()

    query = '%s WHERE user_name = "%s"' % (select, user_name)


    try:
        user = get_one(query)

        return user
    except Exception,e:
        errorMes = str(e)
        print errorMes
        db = get_db()
        cur = db.cursor()
        query = "INSERT INTO VMB.error_messages(\
            file_name, function, message) " \
            "VALUES(%s,%s,%s)"
        args = ('user_info', 'get_user_by_name', errorMes[:100])
        cur.execute(query, args)
        db.commit()

        cur.close()
        db.close()
        return None


def get_user_by_id(user_id=None):

    user_id = int(user_id)
    query = '%s WHERE USERS_id = "%s"' % (select, user_id)

    try:
        user = get_one(query)

        return user
    except Exception,e:
        errorMes = str(e)
        print errorMes
        db = get_db()
        cur = db.cursor()
        query = "INSERT INTO VMB.error_messages(\
            file_name, function, message) " \
            "VALUES(%s,%s,%s)"
        args = ('user_info', 'get_user_by_id', errorMes[:100])
        cur.execute(query, args)
        db.commit()

        cur.close()
        db.close()
        return None

