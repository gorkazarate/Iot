from grove.gpio import GPIO
import sys
import time
import paho.mqtt.client as mqtt

pin =15


# Configuración de MQTT
mqtt_broker ="172.18.0.10"
mqtt_port = 1883
topic_oled = "estado/boton"

def on_connect(client, userdata, flags, rc):
    print(f"Conectado con resultado {rc}") #0 para OK
    client.subscribe(topic_oled)


def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	if ( msg.payload == b'1' ):
		relay.on()
		client.publish("estado/rele", 1,0)
		client.publish("velocidad", 1500,0)
	elif msg.payload == b'0':
		relay.off()
		client.publish("estado/rele", 0,0)
		client.publish("velocidad", 0,0)
#conecct paho
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)
client.subscribe(topic_oled,qos=0)

class GroveRelay(GPIO):
    def __init__(self,pin):
        super(GroveRelay, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)


Grove = GroveRelay
relay = GroveRelay(22) 

def main():

    if len(sys.argv) < 2:
        print('Usage: {} pin'.format(sys.argv[0]))
       

    relay = GroveRelay(int(sys.argv[1]))

    
    try:

        client.loop_forever()

    except KeyboardInterrupt:
        relay.off()
        print("exit")
        exit(1) 

if __name__ == '__main__':
    main()

