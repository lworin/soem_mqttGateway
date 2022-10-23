#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import paho.mqtt.client as mqtt
from DBConnection import DBConnection
from Message import Message

# Configurações da base de dados
dbUsername = "admin"
dbPassword = "123"
dbHost = "localhost"
dbPort = 3306
dbDatabase = "TempSensors"
db = DBConnection(dbUsername, dbPassword, dbHost, dbPort, dbDatabase)

# Configurações do broker MQTT
mqttUser = "admin"
mqttPassword = "123"
mqttHost = "localhost"
mqttPort = 1883
mqttTopic = "mytopics/temp"

# Ao conectar ao broker
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

# Ao assinar um tópico
def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Ao receber mensagem do tópico assinado
def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    mensagem = Message(str(msg.payload.decode('utf8')))
    mensagem.enviar(db)
    
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