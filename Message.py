#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import mariadb
import datetime
from DBConnection import DBConnection

class Message:
    def __init__(self, dados):
        lista = dados.split("#", 1)

        if len(lista) != 2:
            lista = ["0", "0"]
        
        self.setDeviceid(lista[0])
        self.datahora = str(datetime.datetime.now())
        self.setTemperatura(lista[1])
        self.insertString = "INSERT INTO ReceivedData(deviceid, datahora, temperatura) VALUES(?, ? ,?)"

    # Valida e seta o deviceid
    def setDeviceid(self, dev):
        if len(dev) > 0:
            x = int(dev)
        else:
            self.deviceid = 0
            return
        
        if x > 0:
            self.deviceid = x
        else:
            self.deviceid = 0
    
    # Valida e seta a temperatura
    def setTemperatura(self, temp):
        if len(temp) > 0:
            x = float(temp)
        else:
            self.temperatura = 0
            return
        
        if x > 0:
            self.temperatura = x
        else:
            self.temperatura = 0

    # Faz o envio da mensagem
    def enviar(self, db):
        if self.deviceid == 0 or self.temperatura == 0:
            print("Dados invalidos")
            return

        try:
            print("Inserindo: " + str(self.deviceid) + ", " + self.datahora + ", " + str(self.temperatura))
            db.connect()
            db.cursor.execute(self.insertString, (self.deviceid, self.datahora, self.temperatura))
            db.connection.commit()
            print("Dados inseridos")
        except mariadb.Error as ex:
            print(f"Erro ao inserir: {ex}")
            db.connection.close()
            sys.exit(1)
