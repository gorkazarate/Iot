import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import random

# Configuración de MQTT
mqtt_broker ="172.18.0.10"
mqtt_port = 1883
topic_estado_buzzer = "estado/recorrido"



def on_connect(client, userdata, flags, rc):
    print(f"Conectado con resultado {rc}") #0 para OK
    client.subscribe(topic_estado_buzzer)

def on_message(client, userdata, msg):
	numero = random.randint(1,20)
	decibelios = 90 + numero
	if ( msg.payload == b"fuera" ):
		GPIO.output(buzzer_pin, GPIO.HIGH)
		client.publish("estado/buzzer", "1",0)
		client.publish("decibelios", decibelios,0)
	elif ( msg.payload == b"dentro" ):
		GPIO.output(buzzer_pin, GPIO.LOW)
		client.publish("estado/buzzer", "0",0)
		client.publish("decibelios", numero,0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)
client.subscribe(topic_estado_buzzer,qos=0)



#configuracion pines
GPIO.setmode(GPIO.BOARD)
buzzer_pin=19
GPIO.setup(buzzer_pin, GPIO.OUT)


try:
   GPIO.output(buzzer_pin, GPIO.LOW)
   client.loop_forever()
   print("Bucle")
  

except KeyboardInterrupt:
    GPIO.cleanup()
