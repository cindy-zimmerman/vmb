__author__ = 'cz'
import csv
import unicodedata
from accounts import insert_account

def accounts(fileFullName=None):

    with open(fileFullName, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['Casillero'], row['Contacto'])
            if row['Casillero'] != 'PTY-361011':
                Casillero = row['Casillero'].replace("PTY", "")
                Casillero = Casillero.replace("-", "")
                Casillero = Casillero.replace(" ", "")
                casillero = int(Casillero)

                contact = row['Contacto'].replace("\xc3\xb1", chr(241)).replace("\xc3\xb3", chr(243)).replace("\xc3\xad", chr(237))
                Contacto = contact.split()
                contLen = len(Contacto)
                contacto_nombre_1 = ''
                contacto_nombre_2 = ''
                contacto_apellido_1 = ''
                contacto_apellido_2 = ''
                if contLen == 2:
                    contacto_nombre_1 = Contacto[0]
                    contacto_apellido_1 = Contacto[1]
                elif contLen == 3:
                    contacto_nombre_1 = Contacto[0]
                    contacto_nombre_2 = Contacto[1]
                    contacto_apellido_1 = Contacto[2]
                elif contLen == 4:
                    contacto_nombre_1 = Contacto[0]
                    contacto_nombre_2 = Contacto[1]
                    contacto_apellido_1 = Contacto[2]
                    contacto_apellido_2 = Contacto[3]
                else:
                    print 'problem'

                Telefonofij = row['Telefonofij'].replace("-", "")
                Telefonofij = Telefonofij.replace("'", "")
                Telefonofij = Telefonofij.replace(" ", "")
                Telefonofij = Telefonofij.replace("\xc2\xa0", "")
                print Telefonofij
                telefonofij = int(Telefonofij)

                Telefonocel = row['Telefonocel'].replace("-", "")
                Telefonocel = Telefonofij.replace(" ", "")
                telefonocel = int(Telefonocel)

                correo = row['Correo']
                ciudad = row['Ciudad']

                direccion_calle = ''
                direccion_torre = ''
                direccion_apt = ''
                direccion_area = ''

                insert_account(contacto_nombre_1, contacto_nombre_2, contacto_apellido_1,
                                contacto_apellido_2, telefonofij, telefonocel, correo, direccion_calle,
                                direccion_torre, direccion_apt, direccion_area, ciudad, casillero)

if __name__ == "__main__":
    accounts(fileFullName='VMB/currentContacts.csv')
