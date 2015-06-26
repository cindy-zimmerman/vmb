# -*- coding: utf-8 -*-
__author__ = 'cz'
import csv
import math
from invoices import insert_invoices

ACCEPTED_FIELDNAMES = ['N.', 'Fecha', 'Serv', 'Guia', 'Referencia', 'Remitente',
                       'Destinatario', 'Des', 'Peso', 'Piezas', 'Estatus', 'Observacion',
                       'Receptor', 'Fecha_proceso', 'Hora_proceso']

def accounts(fileFullName=None):

    with open(fileFullName) as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        # if reader.fieldnames in ACCEPTED_FIELDNAMES:
        # if ACCEPTED_FIELDNAMES in reader.fieldnames:
        if len(set(ACCEPTED_FIELDNAMES).intersection(reader.fieldnames)) == len(ACCEPTED_FIELDNAMES):

            for row in reader:
                if row['Guia']:

                    fecha = row['Fecha']
                    serv = row['Serv']
                    guia = int(row['Guia'])
                    referencia = row['Referencia'].replace('\xc2\xa0', ' ').replace('\xa0', '')
                    remitente = row['Remitente'].replace('\xc2\xa0', ' ').replace('´', "'").replace('\xb4', "'").replace('\xa0', '')

                    casillero = int(row['Destinatario'].replace("PTY", "").replace('\xc2\xa0', ' ').replace('\xa0', ''))

                    des = row['Des'].replace('\xc2\xa0', ' ').replace('\xa0', '')

                    peso = float(row['Peso'])
                    lb = int(math.ceil((peso * 2.205)))
                    subtotal = lb * 4
                    piezas = int(row['Piezas'].replace('\xc2\xa0', ' ').replace('\xa0', ''))
                    in_panama = 0

                    receptor = row['Receptor'].replace('\xc2\xa0', ' ').replace('\xa0', '')


                    fecha_proceso = row['Fecha_proceso']
                    hora_proceso = row['Hora_proceso']  #TODO change the end

                    paid = amt_paid = 0

                    insert_invoices(serv,guia, referencia, remitente, casillero, des, peso, lb, piezas, in_panama,
                       receptor, fecha, fecha_proceso, hora_proceso, subtotal, paid, amt_paid)
                    count += 1
            else:
                return count

            return count
