import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Configuración de MQTT
mqtt_broker ="172.18.0.10"
mqtt_port = 1883
topic_estado_boton = "estado/boton"
topic_control_led = "control/led"

#configuracion pines
GPIO.setmode(GPIO.BOARD)
boton_pin=11
led_pin=13
GPIO.setup(boton_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_pin, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
    print(f"Conectado con resultado {rc}") #0 para OK
    client.subscribe(topic_estado_boton)


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def on_message(client, userdata, msg):
    if msg.payload == 1 :
        print("Ha entrado")
        GPIO.output(led_pin, GPIO.HIGH)
    elif msg.payload == 0 :
        GPIO.output(led_pin, GPIO.LOW)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)

contador = 0 
memoria = 0
try:
   while True:  
        boton_estado = GPIO.input(boton_pin)
        if (boton_estado == 1 ):
            memoria = 1
            contador = contador +1
        if (boton_estado == 0 & memoria == 1 ):
            memoria = 0
        client.publish("estado/boton", boton_estado,0)
        client.publish("estado/contador", boton_estado,0)
        time.sleep(1)
        
except KeyboardInterrupt:
    GPIO.cleanup()

