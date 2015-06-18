__author__ = 'cz'
from conn import get_db


def insert_account(contacto_nombre_1, contacto_nombre_2, contacto_apellido_1,
            contacto_apellido_2, telefonofij, telefonocel, correo, direccion_calle,
            direccion_torre, direccion_apt, direccion_area, ciudad, casillero=None):

    db = get_db(None)
    cur = db.cursor()

    try:
        if casillero is None:
            cur = db.cursor()
            cur.execute("SELECT MAX(casillero) FROM VMB.VMB_ACCOUNTS")

            cas = cur.fetchone()

            print "casillero : %s " % cas[0]
            casillero = int(cas[0]) + 1
        else:
            if not isinstance(casillero, (int)):
                raise Exception('casillero is not a number')


        if not isinstance(telefonofij, (int)):
            raise Exception('telefonofij is not a number')
        if not isinstance(telefonocel, (int)):
            raise Exception('telefonocel is not a number')

        query = "INSERT INTO VMB.VMB_ACCOUNTS(\
                casillero, contacto_nombre_1, contacto_nombre_2, contacto_apellido_1, \
                contacto_apellido_2, telefonofij, telefonocel, correo, direccion_calle, \
                direccion_torre, direccion_apt, direccion_area, ciudad) " \
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        args = (casillero, contacto_nombre_1, contacto_nombre_2, contacto_apellido_1,
                contacto_apellido_2, telefonofij, telefonocel, correo, direccion_calle,
                direccion_torre, direccion_apt, direccion_area, ciudad)

        # db_config = read_db_config()
        # conn = MySQLConnection(**db_config)

        cursor = db.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        db.commit()
    except Exception,e:
        errorMes = str(e)
        print errorMes
        # TypeError
        query = "INSERT INTO VMB.error_messages(\
            file_name, function, message) " \
            "VALUES(%s,%s,%s)"
        args = ('accounts', 'insert_account', errorMes[:100])
        cursor = db.cursor()
        cursor.execute(query, args)
        db.commit()
    finally:
        cur.close()
        cursor.close()
        db.close()

if __name__ == "__main__":
    contacto_nombre_1 = 'Tomas'
    contacto_nombre_2 = ''
    contacto_apellido_1 = 'Hassan'
    contacto_apellido_2 = ''
    telefonofij = 3141123
    telefonocel = 66195325
    correo = 't.hassan@2oceanmarine.com'
    direccion_calle = 'Calle Pearson & Cars'
    direccion_torre = ''
    direccion_apt = 'Duplex No. 2256 A&B'
    direccion_area = 'Ancon, Balboa'
    ciudad = 'Panama'

    insert_account(contacto_nombre_1, contacto_nombre_2, contacto_apellido_1,
            contacto_apellido_2, telefonofij, telefonocel, correo, direccion_calle,
            direccion_torre, direccion_apt, direccion_area, ciudad)