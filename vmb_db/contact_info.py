__author__ = 'cz'
from vmb_db.conn import get_db, iterate_query, get_one

CLIENTS_PER_PAGE = 50
iter_pages = 100

select = "SELECT " \
            "VMB_ACCOUNTS_id,"\
            "casillero,"\
            "contacto_nombre_1,"\
            "contacto_nombre_2,"\
            "contacto_apellido_1,"\
            "contacto_apellido_2,"\
            "telefonofij,"\
            "telefonocel,"\
            "correo,"\
            "direccion_calle,"\
            "direccion_torre,"\
            "direccion_apt,"\
            "direccion_area,"\
            "ciudad,"\
            "tarifa"\
        " FROM VMB.VMB_ACCOUNTS"

def get_contact_list(where=None, sort=None, limit=None, skip=None):

    if where is None:
        where = " WHERE 1=1"
    else:
        where = " WHERE %s" % (where)

    if sort is None:
        sort = " ORDER BY casillero ASC"
    else:
        sort = " ORDER BY %s" % sort

    if limit:
        sort = '%s LIMIT %s' % (sort, str(int(limit)))
        if skip:
            sort = '%s, %s' % (sort, str(int(skip)))

    try:
        query =  '%s%s%s' % (select, where, sort)
        # https://gist.github.com/robcowie/814599?
        allUsers1 = iterate_query(query=query, connection=None, arraysize=100)
        # contact = row['Contacto'].replace("\xc3\xb1", chr(241)).replace("\xc3\xb3", chr(243)).replace("\xc3\xad", chr(237))
        allUsers = []
        for row_dict in allUsers1:
            user = cleaned_contact(row_dict)
            allUsers.append(user)

        return allUsers
    except Exception,e:
        errorMes = str(e)
        print errorMes
        db = get_db()
        cur = db.cursor()
        query = "INSERT INTO VMB.error_messages(\
            file_name, function, message) " \
            "VALUES(%s,%s,%s)"
        args = ('contact_info', 'get_contact_list', errorMes[:100])
        cur.execute(query, args)
        db.commit()

        cur.close()
        db.close()
        return []


def get_contact(where=None):

    if where is None:
        where = " WHERE 1=1"
    else:
        where = " WHERE %s" % (where)

    try:
        query =  '%s%s' % (select, where)
        user = get_one(query)
        user = cleaned_contact(user)

        return user
    except Exception,e:
        errorMes = str(e)
        print errorMes
        db = get_db()
        cur = db.cursor()
        query = "INSERT INTO VMB.error_messages(\
            file_name, function, message) " \
            "VALUES(%s,%s,%s)"
        args = ('contact_info', 'get_contact', errorMes[:100])
        cur.execute(query, args)
        db.commit()

        cur.close()
        db.close()
        return None

def get_contact_by_casillero(casillero=None):

    if casillero is None:
        casillero = 361010
    else:
        if not isinstance( casillero, int ):
            casillero = casillero.replace("PTY", "").replace("-", "").replace(" ", "")
        where = " WHERE casillero = %s" % (str(casillero))

    try:
        query = '%s%s' % (select, where)
        user = get_one(query)
        user = cleaned_contact(user)

        return user
    except Exception,e:
        errorMes = str(e)
        print errorMes
        db = get_db()
        cur = db.cursor()
        query = "INSERT INTO VMB.error_messages(\
            file_name, function, message) " \
            "VALUES(%s,%s,%s)"
        args = ('contact_info', 'get_contact', errorMes[:100])
        cur.execute(query, args)
        db.commit()

        cur.close()
        db.close()
        return None

def cleaned_contact(contact):

    contact['casillero'] = 'PTY%s' % contact['casillero']

    contact['contacto_nombre_1'] = contact['contacto_apellido_1'].replace("\xf1", 'n').replace("\xf3", 'o').replace("\xed", 'i')
    contact['contacto_nombre_2'] = contact['contacto_apellido_1'].replace("\xf1", 'n').replace("\xf3", 'o').replace("\xed", 'i')
    # contact['contacto_apellido_1'] = contact['contacto_apellido_1'].replace("\xf1", chr(241)).replace("\xf3", chr(243)).replace("\xed", chr(237))
    contact['contacto_apellido_1'] = contact['contacto_apellido_1'].replace("\xf1", 'n').replace("\xf3", 'o').replace("\xed", 'i')
    contact['contacto_apellido_2'] = contact['contacto_apellido_1'].replace("\xf1", 'n').replace("\xf3", 'o').replace("\xed", 'i')
    return contact


