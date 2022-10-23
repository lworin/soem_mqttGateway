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

# Instancia uma conexão
db = DBConnection(dbUsername, dbPassword, dbHost, dbPort, dbDatabase)

# Configurações do broker MQTT
mqttUser = "device"
mqttPassword = "dev123"
mqttHost = "localhost"
mqttPort = 1883
mqttTopic = "temperature"

# Ao conectar ao broker
def on_connect(client, userdata, flags, rc):
    print("Connection return code: " + str(rc))

# Ao assinar um tópico
def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed to: " + mqttTopic + " " + str(mid) + " " + str(granted_qos))

# Ao receber mensagem do tópico assinado
# Instancia um objeto Mensagem e realiza o envio
def on_message(client, obj, msg):
    print("New message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    mensagem = Message(str(msg.payload.decode('utf8')))
    mensagem.enviar(db)
    
# Instancia um cliente MQTT, abre a conexão e assina o tópico
mqttClient = mqtt.Client()
mqttClient.username_pw_set(mqttUser, mqttPassword)
mqttClient.connect(mqttHost, mqttPort)
mqttClient.subscribe(mqttTopic, 0)

# Assina as funções de callback
mqttClient.on_message = on_message
mqttClient.on_connect = on_connect
mqttClient.on_subscribe = on_subscribe

# Mantém o loop MQTT
while True:
    rc = 0
    while rc == 0:
        rc = mqttClient.loop()
    break