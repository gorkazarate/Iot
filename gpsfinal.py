import gpxpy
import gpxpy.gpx
import time
import random
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
import paho.mqtt.client as mqtt
 
# Configuración de MQTT
mqtt_broker ="172.18.0.10"
mqtt_port = 1883

motor = "apagado"

global u_longitud , u_latitud 
u_longitud=0
u_latitud=0
latitud =0 
longitud =0

def on_connect(client, userdata, flags, rc):
    print(f"Conectado con resultado OK") 
    client.subscribe("estado/boton")

def on_message(client, userdata, msg):
    if ( msg.payload ==  b'1' ):
        motor = "encendido"
        print("encendido")
        procesar_gpx(file_path, u_longitud, latitud)
	
    elif ( msg.payload == b'0' ):
        motor = "apagado"
        print("apagado")
    

# Configuramos la visualización en Matplotlib

plt.ion() # Modo interactivo

# Creamos la gráfica para mostrar el recorrido
fig, ax = plt.subplots()
line, = ax.plot([], [], 'bo-') # Puntos azules con líneas

# Cargamos el recorrido desde el archivo GPX
def cargar_recorrido(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

        recorrido_coords = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    recorrido_coords.append((point.longitude, point.latitude))

        u_longitud = recorrido_coords[-1][0]
        u_latitud = recorrido_coords[-1][1]

        return LineString(recorrido_coords)

# Verificamos que la bici no se sale del recorrido que hemos establecido en la ruta gpx
def dentro_del_recorrido(latitud, longitud, recorrido):
    punto_actual = Point(longitud, latitud)
    return punto_actual.within(recorrido)

# Recorremos el archivo GPX
def procesar_gpx(file_path, longitud, latitud):
    recorrido = cargar_recorrido(file_path)
     
    fuera_de_ruta = False # Variable para rastrear si estamos fuera de la ruta

    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                lats, lons = [], [] # Listas para almacenar las coordenadas
                for point in segment.points:

                    # Obtenemos latitud y longitud del punto
                    latitud = point.latitude
                    longitud = point.longitude
                    lats.append(latitud)
                    lons.append(longitud)

                    # Simulamos eventos aleatorios de salirse de la ruta
                    if random.random() < 0.02: # Con un 3% de posibilidades de que la bici se salga debería encenderse el led seguro
                        # Cambiar la posición aleatoriamente (simula salirse de la ruta)
                        latitud += random.uniform(-0.001, 0.001)
                        longitud += random.uniform(-0.001, 0.001)
                        
                        # Indicamos que estamos fuera de la ruta
                        fuera_de_ruta = True
                    else:
                        # Indicamos que estamos dentro de la ruta
                        fuera_de_ruta = False

                    # Verificamos que la bici está dentro del recorrido
                    if dentro_del_recorrido(latitud, longitud, recorrido):
                        print("dentro")
                        client.publish("estado/recorrido", "dentro" ,0)
                        time.sleep(1)
                        u_longitud = point.longitude
                        u_latitud= point.latitude
                        return (u_longitud, u_latitud)
                    else:
                        # Si está fuera
                       print("fuera")
                       client.publish("estado/recorrido", "fuera" ,0)
                       time.sleep(1)
                       u_longitud = point.longitude
                       u_latitud= point.latitude
                       return (u_longitud, u_latitud)

                   
    # Detenemos la visualización interactiva

    plt.ioff()
    plt.show()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)

# Ejecutamos la simulación
if __name__ == "__main__":
    file_path = "/home/unai/recorrido.gpx" 
    client.loop_forever()
    print ("bucle fuera")
    
