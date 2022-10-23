#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import mariadb

# Classe para conexão com o banco de dados
class DBConnection:
    def __init__(self, username, password, host, port, database):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    # Abre coneão com o banco de dados e obtém o cursor
    def connect(self):
        try:
            self.connection = mariadb.connect(user = self.username, password = self.password, host = self.host, port = int(self.port), database = self.database)
            self.cursor = self.connection.cursor()
        except mariadb.Error as ex:
            print(f"Erro ao conectar: {ex}") 
            sys.exit(1)

    # Desconecta do banco de dados
    def disconnect(self):
        self.cursor.close()
        self.connection.close()
