import paho.mqtt.client as mqtt
from brokerData import*            #Informacion de la conexion
from clases import*
import threading #MEPA: Nos permite hacer la concurrencia con hilos------------------------------------
import logging
import time
import sys       #MEPA: Requerido para cuando se ejecute o se levante una excepcion se salga del sitema (sys.exit()) incluso aun cuando los hilos se esten ejecutando en el fondo
import os 

BUFFER_SIZE = 16 * 1024
EnvioA = []

LOG_FILENAME = 'mqtt.log'           #MEPA: LOG de informacion que va a llegar cuando estemos subscritos, lo utilizamos para
                                    #subscribirnos a un topic en especifico o varios y guarda en un archivo de texto-------
                                    #la informacion------------------------------------------------------------------------
TEXT_FILE_USUARIO="usuarios"
TEXT_FILE_SALAS="salas"

#-----------------------------------BASE TOPICS SUBCRITOS---------------------------------------------------------------------
#Nombres de Topics de ejemplo
cmd    = 'comandos'
gr   = '23'
usr     = 'usuarios/23/'
sal = 's'

#-----------------------------------LOGGING-------------------------------------------------------------------------------
logging.basicConfig(                #MEPA: Configuracion inicial de logging, utilizamos threadName porque la libreria paho-
    level = logging.INFO,           #lo utiliza para trabajar
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )
#-----------------------------------CONNECT Y MESSAGE---------------------------------------------------------------------
def on_connect(client, userdata, rc):           #MEPA: Callback que se ejecuta cuando nos conectamos al broker------------
    logging.info("Conexion exitosa")

#Handler en caso se publique satisfactoriamente en el broker MQTT
def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)

def on_message(client, userdata, msg):          #MEPA: #Callback que se ejecuta cuando llega un mensaje al topic subscrito
    #MARP Si estamos subscritos, siempre tiene que existir on_message, aca caeran el mensaje que llegue desde MQTT-------------

    #MARP Se muestra en pantalla informacion que ha llegado
   
    
    Comando = str(msg.payload)
    #print(Comando)
    Listas = (Comando.split('$'))
    #print(Listas)
    a = Listas[0]
    #print(a)
    Listas1 = a.split('x')
    #print(Listas1)
    Ptrama = str(Listas1[1])
    #print(Ptrama)


    if str(Ptrama) == str("08"):
        logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))#MEPA: Nos indica de que topic llego la informacion-- 
        logging.info("El contenido del mensaje es: " + Listas[1]) #MEPA: Nos muestra la informacion que llego----------
        #Tono(1)
    else:
        logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))#MEPA: Nos indica de que topic llego la informacion-- 
        audio = msg.payload
        ConvertirAudio(audio)
        
    #Y se almacena en el log 
    logCommand = 'echo "(' + str(msg.topic) + ') -> ' + str(msg.payload) + '" >> ' + LOG_FILENAME #MEPA: Equivalente a es-
        #escribir en un archivo de texto utilizando la consola de Linux---------------------------------------------------
    os.system(logCommand) #MEPA: Enviamos a os.system el comando para escribir en un archivo de texto la informacion conte
        #nida en logCommand

def Tono(Act = 0):
    if Act == 1:
        os.system('aplay tono.mp3')    


def ConvertirAudio(audio):

    f = open("AudioEnv.mp3","wb") #MARP Open in binary
    f.write(audio)
    f.close

    logging.info('Grabacion finalizada, inicia reproduccion')
    os.system('aplay AudioEnv.mp3')

#-----------------------------------HILOS------------------------------------------------
t1 = threading.Thread(name = 'ALARMA',#MARP Primer hilo que esta asignado a un objeto de tipo
                        target = Tono,           #Thread
                        args = (()),
                        daemon = True
                        )
t2 = threading.Thread(name = 'GRABACION',#MARP Primer hilo que esta asignado a un objeto de tipo
                        target = ConvertirAudio,           #Thread
                        args = ((), ),
                        daemon = True
                        )

t1.start()                          
t2.start()    

#-----------------------------------CONFIGURACION INICIAL (CLIENTE-BROKER)------------------------------------------------
client = mqtt.Client(clean_session=True) #MEPA: Nueva instancia, client nuevo objeto de la clae Client, propia de MQTT----
client.on_connect = on_connect #MEPA: on_connect es un atributo de la clase Client y configura la funcion "Handler" cuando
                               #suceda la conexion, es decir, cuando se conecte un cliente ejecute la accion que se encu--
                               #tre dentro de la funcion on_connect-------------------------------------------------------  
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito-
client.username_pw_set(MQTT_USER, MQTT_PASS) #MEPA: Credenciales requeridas por el broker---------------------------------
client.connect(host=MQTT_HOST, port = MQTT_PORT) #MEPA: Conectar al servidor remoto, si lo dejamos en blanco, automatica--
                                                 #mente se conectara al local host en el puerto 1882----------------------

def publishData(topicRoot, topicName, value, qos = 0, retain = False):
    topic = "usuarios/23/" + topicName
    client.publish(topic, value, qos, retain)

#-----------------------------------SUBSCRIPCION A CANALES----------------------------------------------------------------
    #MEPA: Para subscribirnos a un TOPIC, necesitamos una tupla, en este caso ("sensores/6/hum", qos), donde enviamos dos- 
    #parametros, el primero es el topic al cual nos queremos conectar y el otro es el nivel de qos, los cuales pueden ser- 
    #0,1 y 2. Otra forma de subscribirse es con una lista de tuplas-------------------------------------------------------
qos = 2
usuario=clientes(TEXT_FILE_USUARIO,qos) #BRPG Se hace instancia para suscribir a topic de usuarios
salai=clientes(TEXT_FILE_SALAS,qos) #BRPG Se hace suscripcion para suscribir a topic de clientes
#BRPG Se suscribe a traves de los objetos correspondientes.
client.subscribe('usuarios/23/u',qos)#MEPA: Subscripcion simple con tupla (topic,qos), queremos saber especifica--
print(usuario.getsuscribcionU(TEXT_FILE_USUARIO,qos))
client.subscribe(salai.getsuscribcionaG(TEXT_FILE_SALAS,qos))#mente la variable de humedad de la estacion 6 dentro de la red de sensores------------
print(salai.getsuscribcionaG(TEXT_FILE_SALAS,qos))
#client.subscribe([("sensores/#", qos), ("sensores/+/atm", qos), ("sensores/0/temp", qos)]) #MEPA: Subscripcion multiple-
    #con lista de tuplas, # significa "todo lo que este debajo de eso", en este caso, los tres sensores, veremos como se-- 
    #actualizan los 3 sensores de la estacion 8. + equivalente a * de un nivel, es decir, vamos a ver, de todas las-------
    #estaciones, el sensor de atmosfera-----------------------------------------------------------------------------------

#Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start()  #MEPA: Creamos un diclo infinito que funcionara como un thread demonio, es decir, corre como un hilo-
    #demoneo en el fondo y nos permitira continuar con nuestro programa, loop_start veriifica el status del broker para---
    #ver si no hay informacion que este disponible para nosotros cada cierto tiempo client.loop_forever() hace lo mismo---
    #que client.loop_start() pero la vuelve accion bloqueante-------------------------------------------------------------

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
                publishData(usr, IDdest, "\x08" + "$"  + Mendest)
                logging.info('Codigo para enviar a usuario')
            if Respuestaf2_1 == '02':
                IDdest = input('Ingrese el ID de la sala destino: ')
                Mendest = input('Ingrese el MENSAJE PARA la sala destino: ')
                publishData(IDdest, gr, "\x08" + "$"  + Mendest)

        if Respuestaf1 == '02':
            logInfo01 = '\n\n Enviar a usuario (01) \n\n Enviar a Sala(02)'
            logging.info(logInfo01)
            textoR = input('Ingrese codigo de accion:')
            if textoR == '01':
                IDdest = input('Ingrese el ID del usuario destino: ')               
                grabacion(IDdest)
            if textoR == '02':
                duracionR = input('Ingrese la duracion de la grabacion (s) para sala:')

def enviar(array, remitente,destinatario):
        for i in array:
            publishData(remitente, destinatario,i)

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
   
    enviar(lista,usr,IDdest)
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
#t2.start()

DEFAULT_DELAY = 6 #1 minuto
#MARP Loop principal: leer los datos de los sensores y enviarlos al broker en los topics adecuados cada cierto tiempo
try:
    while True:
        #logging.info("olakease")
        time.sleep(DEFAULT_DELAY)

except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop()                      #MARP Se mata el hilo que verifica los topics en el fondo
    client.disconnect()                     #MARP Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")