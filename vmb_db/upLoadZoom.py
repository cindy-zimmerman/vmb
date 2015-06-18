__author__ = 'cz'
import csv
import math
from invoices import insert_invoices

def accounts(fileFullName=None):

    with open(fileFullName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print row
            # guia = row['Guia']
            if row['Guia']:

                fecha = row['Fecha']
                serv = row['Serv']
                guia = int(row['Guia'])
                referencia = row['Referencia'].replace('\xc2\xa0', ' ')
                remitente = row['Remitente'].replace('\xc2\xa0', ' ')

                casillero = int(row['Destinatario'].replace("PTY", "").replace('\xc2\xa0', ' '))
                # print casillero

                des = row['Des'].replace('\xc2\xa0', ' ')

                peso = float(row['Peso'])
                lb = int(math.ceil((peso * 2.205)))
                subtotal = lb * 4
                piezas = int(row['Piezas'].replace('\xc2\xa0', ' '))

                status = row['Estatus'].replace('\xc2\xa0', ' ').split()
                if status[0] == 'ENTREGADO':
                    in_panama = 1
                else:
                    in_panama = 0

                receptor = row['Receptor'].replace('\xc2\xa0', ' ')


                fecha_proceso = row['Fecha proceso']
                hora_proceso = row['Hora proceso'] #TODO change the end

                paid = amt_paid = 0

                insert_invoices(serv,guia, referencia, remitente, casillero, des, peso, lb, piezas, in_panama,
                   receptor, fecha, fecha_proceso, hora_proceso, subtotal, paid, amt_paid)




if __name__ == "__main__":
    accounts(fileFullName='VMB/zoom1.csv')
