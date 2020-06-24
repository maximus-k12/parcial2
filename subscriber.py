import paho.mqtt.client as mqtt
import logging
import time
import os 
from brokerData import *            #Informacion de la conexion

LOG_FILENAME = 'mqtt.log'           #MEPA: LOG de informacion que va a llegar cuando estemos subscritos, lo utilizamos para
                                    #subscribirnos a un topic en especifico o varios y guarda en un archivo de texto-------
                                    #la informacion------------------------------------------------------------------------

#-----------------------------------LOGGING-------------------------------------------------------------------------------
logging.basicConfig(                #MEPA: Configuracion inicial de logging, utilizamos threadName porque la libreria paho-
    level = logging.INFO,           #lo utiliza para trabajar
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )
#-----------------------------------CONNECT Y MESSAGE---------------------------------------------------------------------
def on_connect(client, userdata, rc):           #MEPA: Callback que se ejecuta cuando nos conectamos al broker------------
    logging.info("Conectado al broker")

def on_message(client, userdata, msg):          #MEPA: #Callback que se ejecuta cuando llega un mensaje al topic subscrito
    #Si estamos subscritos, siempre tiene que existir on_message, aca caeran el mensaje que llegue desde MQTT-------------

    #Se muestra en pantalla informacion que ha llegado
    logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))#MEPA: Nos indica de que topic llego la informacion-- 
    logging.info("El contenido del mensaje es: " + str(msg.payload)) #MEPA: Nos muestra la informacion que llego----------
    print("\n\n")
    print("\n\n")
    print("\n\n")
    print("\n\n")
    print("\n\n")
    ConvertirAudio(msg.payload)
    #Y se almacena en el log 

    logCommand = 'echo "(' + str(msg.topic) + ') -> ' + str(msg.payload) + '" >> ' + LOG_FILENAME #MEPA: Equivalente a es-
        #escribir en un archivo de texto utilizando la consola de Linux---------------------------------------------------
    os.system(logCommand) #MEPA: Enviamos a os.system el comando para escribir en un archivo de texto la informacion conte
        #nida en logCommand

def ConvertirAudio(audio):
    print(type(audio))
    print(audio)

    f = open("mierda.mp3","wb") # Open in binary

    #while ():
    f.write(audio)
        #l = connection.recv(BUFFER_SIZE)
    #    print('Reciviendo...')
    #    i = i +1
    f.close

    logging.info('Grabacion finalizada, inicia reproduccion')
    os.system('aplay mierda.mp3')
    

#-----------------------------------CONFIGURACION INICIAL (CLIENTE-BROKER)------------------------------------------------
client = mqtt.Client(clean_session=True) #MEPA: Nueva instancia, client nuevo objeto de la clae Client, propia de MQTT----
client.on_connect = on_connect #MEPA: on_connect es un atributo de la clase Client y configura la funcion "Handler" cuando
                               #suceda la conexion, es decir, cuando se conecte un cliente ejecute la accion que se encu--
                               #tre dentro de la funcion on_connect-------------------------------------------------------  
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito-
client.username_pw_set(MQTT_USER, MQTT_PASS) #MEPA: Credenciales requeridas por el broker---------------------------------
client.connect(host=MQTT_HOST, port = MQTT_PORT) #MEPA: Conectar al servidor remoto, si lo dejamos en blanco, automatica--
                                                 #mente se conectara al local host en el puerto 1882----------------------

#-----------------------------------SUBSCRIPCION A CANALES----------------------------------------------------------------
    #MEPA: Para subscribirnos a un TOPIC, necesitamos una tupla, en este caso ("sensores/6/hum", qos), donde enviamos dos- 
    #parametros, el primero es el topic al cual nos queremos conectar y el otro es el nivel de qos, los cuales pueden ser- 
    #0,1 y 2. Otra forma de subscribirse es con una lista de tuplas-------------------------------------------------------
qos = 2
client.subscribe(("usuarios/201444696", qos))#MEPA: Subscripcion simple con tupla (topic,qos), queremos saber especifica--
client.subscribe(("salas/23", qos))#mente la variable de humedad de la estacion 6 dentro de la red de sensores------------
#client.subscribe([("sensores/#", qos), ("sensores/+/atm", qos), ("sensores/0/temp", qos)]) #MEPA: Subscripcion multiple-
    #con lista de tuplas, # significa "todo lo que este debajo de eso", en este caso, los tres sensores, veremos como se-- 
    #actualizan los 3 sensores de la estacion 8. + equivalente a * de un nivel, es decir, vamos a ver, de todas las-------
    #estaciones, el sensor de atmosfera-----------------------------------------------------------------------------------

#Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start()  #MEPA: Creamos un diclo infinito que funcionara como un thread demonio, es decir, corre como un hilo-
    #demoneo en el fondo y nos permitira continuar con nuestro programa, loop_start veriifica el status del broker para---
    #ver si no hay informacion que este disponible para nosotros cada cierto tiempo client.loop_forever() hace lo mismo---
    #que client.loop_start() pero la vuelve accion bloqueante-------------------------------------------------------------

try:
    while True:
        logging.info("olakease")
        time.sleep(10)


except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop()                      #Se mata el hilo que verifica los topics en el fondo
    client.disconnect()                     #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")