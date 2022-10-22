#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import mariadb
import paho.mqtt.client as mqtt

# Configurações da base de dados
dbUser = "luan"
dbPassword = "123"
dbHost = "localhost"
dbPort = 3306
dbDatabase = "mydb"

# Configurações do broker MQTT
mqttUser = "admin"
mqttPassword = "123"
mqttHost = "localhost"
mqttPort = 1883
mqttTopic = "mytopics/temp"

# Abre a conexão com a base de dados
def dbConectar():
    try:
        dbCon = mariadb.connect(user = dbUser, password = dbPassword, host = dbHost, port = int(dbPort), database = dbDatabase)
        return dbCon
    except mariadb.Error as ex:
        print(f"Erro ao conectar: {ex}") 
        sys.exit(1)

# Insere os dados passados na base de dados
def dbInserir(dados):
    
    dbCon = dbConectar()
    print("Conectado ao banco de dados")
    dbCon.autocommit = False
    dbCur = dbCon.cursor()

    try:
        dbCur.execute("insert into sensors(id, datahora, temperatura) values(?, ? ,?)", (int(dados[0]), dados[1], int(dados[2])))
        dbCon.commit()
        print("Dados inseridos")
    except mariadb.Error as ex:
        print(f"Erro ao inserir: {ex}")
        dbCon.close()
        sys.exit(1)
    
    dbCon.close()
    print("Desconectado do banco de dados")

# Ao conectar ao broker
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

# Ao assinar um tópico
def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Ao receber mensagem do tópico assinado
def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    dados = str(msg.payload.decode('utf8')).split("#", 2)
    print(dados)
    dbInserir(dados)
    
# Define um cliente MQTT, abre a conexão e assina o tópico
mqttClient = mqtt.Client()
mqttClient.username_pw_set(mqttUser, mqttPassword)
mqttClient.connect(mqttHost, mqttPort)
mqttClient.subscribe(mqttTopic, 0)

# Assina as funções de callback
mqttClient.on_message = on_message
mqttClient.on_connect = on_connect
mqttClient.on_subscribe = on_subscribe

while True:
    rc = 0
    while rc == 0:
        rc = mqttClient.loop()
    break