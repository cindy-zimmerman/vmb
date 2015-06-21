__author__ = 'cz'
from vmb_db.conn import get_db, iterate_query, get_one, error_mess

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
        error_mess(pythonFile='contact_info', function='get_contact_list', errorMess=errorMes[:100])
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

        error_mess(pythonFile='contact_info', function='get_contact', errorMess=errorMes[:100])
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
        error_mess(pythonFile='contact_info', function='get_contact_by_casillero', errorMess=errorMes[:100])
        return None

def cleaned_contact(contact):

    contact['casillero'] = 'PTY%s' % contact['casillero']

    contact['contacto_nombre_1'] = contact['contacto_nombre_1'].replace("\xf1", 'n').replace("\xf3", 'o').replace("\xed", 'i')
    contact['contacto_nombre_2'] = contact['contacto_nombre_2'].replace("\xf1", 'n').replace("\xf3", 'o').replace("\xed", 'i')
    # contact['contacto_apellido_1'] = contact['contacto_apellido_1'].replace("\xf1", chr(241)).replace("\xf3", chr(243)).replace("\xed", chr(237))
    contact['contacto_apellido_1'] = contact['contacto_apellido_1'].replace("\xf1", 'n').replace("\xf3", 'o').replace("\xed", 'i')
    contact['contacto_apellido_2'] = contact['contacto_apellido_2'].replace("\xf1", 'n').replace("\xf3", 'o').replace("\xed", 'i')

    contact['direccion_calle'] = contact['direccion_calle'].replace("\xf1", 'n').replace("\xf3", 'o').replace("\xed", 'i')
    contact['direccion_torre'] = contact['direccion_torre'].replace("\xf1", 'n').replace("\xf3", 'o').replace("\xed", 'i')
    contact['direccion_apt'] = contact['direccion_apt'].replace("\xf1", 'n').replace("\xf3", 'o').replace("\xed", 'i')
    contact['direccion_area'] = contact['direccion_area'].replace("\xf1", 'n').replace("\xf3", 'o').replace("\xed", 'i')
    return contact


def set_contact_by_casillero(newClient, casillero=None, updatedUser=None):

    if casillero is None:
        raise Exception('casillero is None')
    else:
        if not isinstance( casillero, int ):
            casillero = casillero.replace("PTY", "").replace("-", "").replace(" ", "")
            casillero = int(casillero)

    args2 = [casillero, newClient['contacto_nombre_1'], newClient['contacto_nombre_2'],
            newClient['contacto_apellido_1'], newClient['contacto_apellido_2'],
            newClient['telefonofij'], newClient['telefonocel'], newClient['correo'],
            newClient['direccion_calle'], newClient['direccion_torre'],
            newClient['direccion_apt'], newClient['direccion_area'], newClient['tarifa'],
            updatedUser, 0]

    try:
        db = get_db(None)
        cur = db.cursor()

        results = cur.callproc('update_cont_by_cas', args2)

        cur.close()
        db.close()

        return results[0]
    except Exception,e:
        db.rollback()
        errorMes = str(e)
        print errorMes
        db = get_db()
        error_mess(pythonFile='contact_info', function='set_contact_by_casillero', errorMess=errorMes[:100])

        cur.close()
        db.close()
        return 0


