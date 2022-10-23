#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import mariadb
from DBConnection import DBConnection

class Message:
    def __init__(self, dados):
        lista = dados.split("#", 2)
        self.deviceid = int(lista[0])
        self.datahora = lista[1]
        self.temperatura = float(lista[2])
        self.insertString = "INSERT INTO ReceivedData(deviceid, datahora, temperatura) VALUES(?, ? ,?)"

    def enviar(self, db):
        try:
            db.connect()
            db.cursor.execute(self.insertString, (self.deviceid, self.datahora, self.temperatura))
            db.connection.commit()
            print("Dados inseridos")
        except mariadb.Error as ex:
            print(f"Erro ao inserir: {ex}")
            db.connection.close()
            sys.exit(1)
