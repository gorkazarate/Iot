import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import Adafruit_SSD1306 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess


GPIO.setmode(GPIO.BOARD)
led_pin=37
GPIO.setup(led_pin, GPIO.OUT)

# Configuración de MQTT
mqtt_broker ="172.18.0.10"
mqtt_port = 1883
topic_oled = "estado/boton"


def on_connect(client, userdata, flags, rc):
    print(f"Conectado con resultado {rc}") #0 para OK
    client.subscribe(topic_oled)

def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	GPIO.output(led_pin, GPIO.HIGH)
	if ( msg.payload == b'1' ):
		draw.rectangle((0, 0, width, height), outline=0, fill=0)
		draw.text((x, top), "Motor en marcha" ,font=font, fill=255)
		disp.image(image)
		disp.display()
		client.publish("estado/oled", "Oled Funcionando",0)
		client.publish("estado/oled/msj", "Boton Pulsado, Motor Encendido",0)
		GPIO.output(led_pin, GPIO.HIGH)
	elif msg.payload == b'0':
		draw.rectangle((0, 0, width, height), outline=0, fill=0)
		draw.text((x, top), "Motor Apagado" ,font=font, fill=255)
		disp.image(image)
		disp.display()
		client.publish("estado/oled", "Oled Funcionando",0)
		client.publish("estado/oled/msj", "Boton Suelto, Motor Apagado",0)
		GPIO.output(led_pin, GPIO.LOW)

# Initialize library.
disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=1, gpio=1)
disp.begin()

# Clear display.
disp.clear()
disp.display()
width = disp.width
height = disp.height
padding = -2
top = padding
bottom = height-padding
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)
x = 0
font = ImageFont.load_default()

#conecct paho
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)
client.subscribe(topic_oled,qos=0)

#Bucle principal str()
try:	
	client.loop_forever()
	print ("bucle fuera")

except KeyboardInterrupt:
    GPIO.cleanup()
