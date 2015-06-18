__author__ = 'cz'

from vmb_db.conn import get_db, iterate_query, get_one
INVOICES_PER_PAGE = 50

select = "SELECT " \
            "INVOICES_id,"\
            "serv,"\
            "guia,"\
            "referencia,"\
            "remitente,"\
            "casillero,"\
            "des,"\
            "peso,"\
            "lb,"\
            "piezas,"\
            "IF(in_panama = 1,'Si','No') AS in_panama,"\
            "receptor,"\
            "fecha,"\
            "fecha_proceso,"\
            "hora_proceso,"\
            "subtotal,"\
            "IF(paid = 1,'Si','No') AS paid,"\
            "amt_paid,"\
            "VMB_ACCOUNTS_id,"\
            "invoice_num "\
        "FROM VMB.INVOICES"



def get_invoice_list(where=None, sort=None, limit=None, skip=None):

    if where is None:
        where = " WHERE 1=1"
    else:
        where = " WHERE %s" % (where)

    if sort is None:
        sort = " ORDER BY invoice_num DESC"
    else:
        sort = " ORDER BY %s" % sort

    if limit:
        sort = '%s LIMIT %s' % (sort, str(int(limit)))
        if skip:
            sort = '%s, %s' % (sort, str(int(skip)))

    try:
        query =  '%s%s%s' % (select, where, sort)
        # https://gist.github.com/robcowie/814599?
        return iterate_query(query=query, connection=None, arraysize=100)
    except Exception,e:
        errorMes = str(e)
        print errorMes
        db = get_db()
        cur = db.cursor()
        query = "INSERT INTO VMB.error_messages(\
            file_name, function, message) " \
            "VALUES(%s,%s,%s)"
        args = ('invoice_info', 'get_invoice_list', errorMes[:100])
        cur.execute(query, args)
        db.commit()

        cur.close()
        db.close()
        return []


def get_invoice_list_by_casillero(casillero=None, sort=None, limit=None, skip=None):

    if casillero is None:
        casillero = 361010
    else:
        if not isinstance( casillero, int ):
            casillero = casillero.replace("PTY", "").replace("-", "").replace(" ", "")
        where = " WHERE casillero = %s" % (str(casillero))

    if sort is None:
        sort = " ORDER BY invoice_num DESC"
    else:
        sort = " ORDER BY %s" % sort

    if limit:
        sort = '%s LIMIT %s' % (sort, str(int(limit)))
        if skip:
            sort = '%s, %s' % (sort, str(int(skip)))

    try:
        query = '%s%s%s' % (select, where, sort)
        print query
        # https://gist.github.com/robcowie/814599?
        return iterate_query(query=query, connection=None, arraysize=100)
    except Exception,e:
        errorMes = str(e)
        print errorMes
        db = get_db()
        cur = db.cursor()
        query = "INSERT INTO VMB.error_messages(\
            file_name, function, message) " \
            "VALUES(%s,%s,%s)"
        args = ('invoice_info', 'get_invoice_list_by_casillero', errorMes[:100])
        cur.execute(query, args)
        db.commit()

        cur.close()
        db.close()
        return []


if __name__ == '__main__':
    page = 1
    CLIENTS_PER_PAGE = 50
    # all = get_contact_list(where=None, sort=None, limit=50, skip=(page - 1) * CLIENTS_PER_PAGE)
    # for i in all:
    #     print i
    inv = get_invoice_list_by_casillero(casillero=361053)
    for i in inv:
        print i