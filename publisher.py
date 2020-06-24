"""*****************************Publisher Parcial 2**********************************"""

import paho.mqtt.client as paho
import threading #MEPA: Nos permite hacer la concurrencia con hilos------------------------------------
import logging
import time
import sys       #MEPA: Requerido para cuando se ejecute o se levante una excepcion se salga del sitema (sys.exit()) incluso aun cuando los hilos se esten ejecutando en el fondo
import os

from brokerData import * #Informacion de la conexion

BUFFER_SIZE = 16 * 1024
EnvioA = []


#-----------------------------------BASE TOPICS SUBCRITOS---------------------------------------------------------------------
#Nombres de Topics de ejemplo
cmd    = 'comandos'
gr   = '23'
usr     = 'usuarios'
sal = 'salas'

#-----------------------------------CONNECT Y PUBLISH---------------------------------------------------------------------
#Handler en caso suceda la conexion con el broker MQTT
def on_connect(client, userdata, flags, rc): 
    connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
    logging.info(connectionText)

#Handler en caso se publique satisfactoriamente en el broker MQTT
def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)

#-----------------------------------LOGGING-------------------------------------------------------------------------------
#Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )

#-----------------------------------CONFIG. INICIAL DEL CLIENTE MQTT------------------------------------------------------
client = paho.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto

def publishData(topicRoot, topicName, value, qos = 0, retain = False):
    topic = topicRoot + "/" + topicName
    client.publish(topic, value, qos, retain)

#-----------------------------------CONSOLA------------------------------------------------
def Interfaz(): 
    while True:
        logging.info('\n\n Enviar texto(01) \n\n Enviar mensaje de voz(02) \n\n Salir(03) \n\n')    #MEPA: mensajes al usuario
        Respuestaf1 = input('Ingrese codigo de accion:')

        if Respuestaf1 == '01':
            logging.info('\n\n Enviar a usuario (01) \n\n Enviar a Sala(02)')
            Respuestaf2_1 = input('Ingrese el codigo del destino:')
            if Respuestaf2_1 == '01':
                IDdest = input('Ingrese el ID del usuario destino: ')
                Mendest = input('Ingrese el MENSAJE PARA el usuario destino: ')
                publishData(usr, IDdest, Mendest)
                logging.info('Codigo para enviar a usuario')
            if Respuestaf2_1 == '02':
                IDdest = input('Ingrese el ID de la sala destino: ')
                Mendest = input('Ingrese el MENSAJE PARA la sala destino: ')
                publishData(sal, gr, Mendest)

        if Respuestaf1 == '02':
            logInfo01 = '\n\n Enviar a usuario (01) \n\n Enviar a Sala(02)'
            logging.info(logInfo01)
            textoR = input('Ingrese codigo de accion:')
            if textoR == '01':
                IDdest = input('Ingrese el ID del usuario destino: ')               
                grabacion(IDdest)
                #t2.start()
                #duracionR = input('Ingrese la duracion de la grabacion(s) para usuario:')
            if textoR == '02':
                duracionR = input('Ingrese la duracion de la grabacion (s) para sala:')

#-----------------------------------GRABACION------------------------------------------------
def grabacion(IDdest): 
    lista = []
    lista1 = []
    tuplamusica = []

    logging.info('Comenzando grabacion')
    os.system('arecord -d 10 -f U8 -r 8000 prueba.mp3')

    print("\n\n")
    f = open ("prueba.mp3", "rb")
    l = f.read(BUFFER_SIZE)

    while (l):
        #sock.sendall(l)
        l = f.read(BUFFER_SIZE)
        lista.append(l)
        print('Enviando...')
    f.close()
    
    print(lista[0])

    lista1 = [lista[0] + lista[1] + lista[3] + lista[4]]
   

    publishData(usr, IDdest,lista1[0])
    #i=0
    #while i <= len(lista)-1 :
    #    publishData(usr, IDdest,lista[i])
    #    i = i + 1
    
   
#-----------------------------------HILOS------------------------------------------------
t1 = threading.Thread(name = 'CONSOLA',#Primer hilo que esta asignado a un objeto de tipo
                        target = Interfaz,           #Thread
                        args = (() ),
                        daemon = True
                        )
t2 = threading.Thread(name = 'GRABACION',#Primer hilo que esta asignado a un objeto de tipo
                        target = grabacion,           #Thread
                        args = (() ),
                        daemon = True
                        )
                        
t1.start()


#Cantidad de sensores de ejemplo que se simulan
CNT_SENSORES = 10

#Tiempo de espera entre lectura y envio de dato de sensores a broker (en segundos)
DEFAULT_DELAY = 6 #1 minuto


logging.info("Cliente MQTT con paho-mqtt") #Mensaje en consola




#Mensaje de prueba MQTT en el topic "test"
client.publish("test", "Mensaje inicial", qos = 0, retain = False)

#Loop principal: leer los datos de los sensores y enviarlos al broker en los topics adecuados cada cierto tiempo
try:
    while True:
        
        #Para presion
    #    for i in range(sensores.getSensorCount()):
    #publishData(SENSORES, (str(i) + "/" + PRESION_A), sensores.getPresionA(i))
        publishData(("comandos"), ("23" + "/" + "201503831"), ("PUTOS MIERDAS"))


        #logging.info("Los datos han sido enviados al broker")            

        #Retardo hasta la proxima publicacion de info
        time.sleep(DEFAULT_DELAY)

except KeyboardInterrupt:
    logging.warning("Desconectando del broker MQTT...")

finally:
    client.disconnect()
    logging.info("Se ha desconectado del broker. Saliendo...")