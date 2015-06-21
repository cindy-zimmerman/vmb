__author__ = 'cz'
from vmb_db.conn import get_db, get_one, error_mess

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
        error_mess(pythonFile='user_info', function='get_user_by_name', errorMess=errorMes[:100])
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
        error_mess(pythonFile='user_info', function='get_user_by_id', errorMess=errorMes[:100])
        return None

