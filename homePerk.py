import time #se necesita para usar las funciones de tiempo
from subprocess import call #la necesitamos para la interrupcion de teclado
import RPi.GPIO as GPIO
import os #usado para limpiar interfaz y otros comandos del OS
global start


GPIO.setmode(GPIO.BOARD) #Queremos usar la numeracion de la placa
 
#Definimos los dos pines del sensor que hemos conectado: Trigger y Echo
Trig = 7
Echo1 = 12
Echo2 = 16



#Hay que configurar ambos pines del HC-SR04
GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo1, GPIO.IN)
GPIO.setup(Echo2, GPIO.IN)
 
#Para leer la distancia del sensor al objeto, creamos una funcion
def detectarObstaculo(Echo):
    global medidaT1
    global medidaT2
    start = 0
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Trig, GPIO.OUT)
    GPIO.setup(Echo1, GPIO.IN)
    GPIO.setup(Echo2, GPIO.IN)
    ##print("enviando pulso...")
    GPIO.output(Trig, False) #apagamos el pin Trig
    time.sleep(2*10**-6) #esperamos dos microsegundos
    GPIO.output(Trig, True) #encendemos el pin Trig
    time.sleep(10*10**-6) #esperamos diez microsegundos
    GPIO.output(Trig, False) #y lo volvemos a apagar
    #empezaremos a contar el tiempo cuando el pin Echo se encienda
    ##print("pulso enviado!")
    while GPIO.input(Echo) == 0:
        start = time.time()

    while GPIO.input(Echo) == 1:
        end = time.time()
    ##print("realizando calculos")
    #La duracion del pulso del pin Echo sera la diferencia entre
    #el tiempo de inicio y el final
    duracion = end-start
    ##print("duracion: "+str(duracion)+ str("ms"))

    #Este tiempo viene dado en segundos. Si lo pasamos
    #a microsegundos, podemos aplicar directamente las formulas
    #de la documentacion
    duracionAlf = duracion*10**6
    medida = duracionAlf/58 #hay que dividir por la constante que pone en la documentacion, nos dara la distancia en cm
    ##print("calculo hecho")
    if Echo == Echo1:
        Sens= str("Sensor 1")
        medidaT1=float(medida)
        #return medidaT1
    if Echo == Echo2:
        Sens= str("Sensor 2")
        medidaT2=medida
        #return medidaT2
    #print(str("%.2f" %medida)+" En "+str(Sens)) #por ultimo, vamos a mostrar el resultado por pantalla

    #Bucle principal del programa, lee el sensor. Se sale con CTRL+C
Play=int(1)
while True or Play == int(1):

    
    try:
        detectarObstaculo(Echo1)
        #detectarObstaculo(Echo2)
        time.sleep(1)
        medidaTT1=medidaT1
        medidaTT2=medidaT1
        print(medidaTT1)
        print(medidaTT2)
        if medidaT1 <= float(350):
            os.system("clear")
            print(""""
         ----Bienvenido al Smart Parking homePerk---
            
            El puesto Nro. 1 esta //OCUPADO//
            
         #######################################       
         #            #           # ///////////#
         #      3     #     2     # /////1/////#
         #            #           # ///////////#
         #######################################         
          
        Version: alpha 0.1      por Polarium ISC
        

     *esta aplicacion se encuentra en fase
     alpha, por lo que se esperan bugs y 
     glitches que han de ser corregidos en
     futuras versiones.""")
        if medidaT1 >= float(350):
            os.system("clear")
            print("""
         ----Bienvenido al Smart Parking homePerk--- 

            El puesto Nro. 1 esta --LIBRE--
                     
         #######################################       
         #            #           #            #
         #      3     #     2     #      1     #
         #            #           #            #
         #######################################         
          
        Version: alpha 0.1      por Polarium ISC
      
        
     *esta aplicacion se encuentra en fase
     alpha, por lo que se esperan bugs y 
     glitches que han de ser corregidos en
     futuras versiones.""")
 #       if medidaTT2 <= float(350):
 #           print("""            El puesto Nro. 2 esta //OCUPADO//
 #           
 #           """)
 #       if medidaTT2 >= float(350):
 #           print("""            El puesto Nro. 2 esta --LIBRE--
 #           
 #           """)
    except KeyboardInterrupt:
        break

#se restablecen los pines GPIO
print("Limpiando...")
GPIO.cleanup()
print("Acabado.")
