__author__ = 'cz'
from conn import get_db, error_mess
import time, datetime


def insert_invoices(serv, guia, referencia, remitente, casillero, des, peso, lb, piezas, in_panama,
                   receptor, fecha, fecha_proceso, hora_proceso, subtotal, paid, amt_paid):

    db = get_db(None)
    cur = db.cursor()

    try:
        fecha_list = fecha.split("/")
        fecha_date = datetime.datetime((int(fecha_list[2]) + 2000), int(fecha_list[1]), int(fecha_list[0]))
        fecha_str = fecha_date.date().isoformat()

        fecha_proceso_list = fecha_proceso.split("/")
        fecha_proceso_date = datetime.datetime((int(fecha_proceso_list[2]) + 2000), int(fecha_proceso_list[1]),
                                               int(fecha_proceso_list[0]))
        fecha_proceso_str = fecha_proceso_date.date().isoformat()

        if hora_proceso[-1] == ':':
            horas = hora_proceso.split(":")
            if horas[1].find("PM"):
                print int(horas[0])
                hour = str(int(horas[0]) + 12)
            else:
                print horas[0]
                hour = horas[0]
            min = horas[1].replace("PM", "").replace("AM", "")
            horas_redone = '%s:%s:00' % (hour, min)
            # print horas_redone
            # t = time.strptime(horas_redone, "%H:%M:%S")
            hora_proceso_str = horas_redone
        else:
            # horas = hora_proceso.split(":")
            # print hora_proceso
            # t = time.mktime(time.strptime(hora_proceso, "%H:%M:%S"))
            # print t
            hora_proceso_str = hora_proceso

        if not isinstance(casillero, int):
            raise Exception('casillero is not a number')

        findUser = "SELECT VMB_ACCOUNTS_id FROM VMB.VMB_ACCOUNTS where casillero = %s"
        cur.execute(findUser, casillero)
        user = cur.fetchone()
        VMB_ACCOUNTS_id = int(user[0])

        findInvoice = "SELECT INVOICES_id FROM VMB.INVOICES where guia = %s"
        cur.execute(findInvoice, guia)
        invoice = cur.fetchone()



        if invoice:
            INVOICES_id = int(invoice[0])
            query = "UPDATE VMB.INVOICES \
                     SET receptor=%s, \
                     fecha=%s, fecha_proceso=%s, hora_proceso=%s \
                     WHERE INVOICES_id=%s"
            args = (receptor, fecha_str, fecha_proceso_str, hora_proceso_str, INVOICES_id)
        else:
            query = "INSERT INTO VMB.INVOICES(\
                    serv, guia, referencia, remitente, casillero, des, peso, lb, piezas, in_panama, \
                    receptor, fecha, fecha_proceso, hora_proceso, subtotal, paid, amt_paid, VMB_ACCOUNTS_id) " \
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (serv, guia, referencia, remitente, casillero, des, peso, lb, piezas, in_panama,
                    receptor, fecha_str, fecha_proceso_str, hora_proceso_str, subtotal, paid, amt_paid, VMB_ACCOUNTS_id)


        cur.execute(query, args)

        if cur.lastrowid:
            print('last insert id', cur.lastrowid)
        else:
            print('last insert id not found')

        db.commit()
    except Exception,e:
        errorMes = str(e)
        print errorMes
        # TypeError
        error_mess(pythonFile='invoices', function='insert_invoices', errorMess=errorMes[:100])
    finally:
        cur.close()
        db.close()

