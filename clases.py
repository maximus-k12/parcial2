#----------------------------------------------------SUSCRIPCION-----------------------------------------------------------
class clientes(object): #BRPG Esta clase se utiliza para realizar asuntos de suscripcion.
    def __init__(self, parametro, politica): #BRPG El parametro politica hace referencia a qos. En cambio parametro es una archivo 
        self.parametro = parametro
        self.politica = politica

    def getDatos(self, parametro):#BRPG Esta funcion permite generar una lista de todas las lineas en un archivo
        vectorInfo =[]
        for linea in parametro:
            segmento=linea.split('\n')
            segmento=segmento[0]
            vectorInfo.append(segmento)
        return vectorInfo 
    
    def getsuscribcionU(self, parametro, politica): #BRPG Aqui se define el metodo para suscribir a usuarios
        lines = self.getDatos(self.parametro)
        suscripcion = []
        for i in lines:
            suscripcion.append(("usuarios/23/" + str(i),self.politica))
        return suscripcion 

    def getsuscribcionaG(self, parametro, politica): #BRPG Aqui se define el metodo para suscribir a cada usuario a su sala.
        lines = self.getDatos(self.parametro) 
        suscripcion = []
        for i in lines:
            suscripcion.append((str(i)+"/23",self.politica))
        return suscripcion 

    