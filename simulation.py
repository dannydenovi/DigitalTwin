from coppeliasim_zmqremoteapi_client import *
from paho.mqtt import client as mqtt_client

#MQTT SETTINGS
broker = '192.168.1.221'
port = 1883
topics =["door", "main_light", "air_conditioner"]
client_id = f'macbook'

# COPPELIA CONNECTION
client = RemoteAPIClient()
sim = client.getObject('sim')
sim.startSimulation()
door = sim.getObject('/door/doorJoint')
main_light = sim.getObject('/main_light')
air_conditioner_status = sim.getObject('/air_conditioner_status')
COLOR_COMPONENT = sim.colorcomponent_ambient_diffuse


# COLORS DEFINITION
MAIN_LIGHT_ON = [1, 1, 0]
COLD_AIR      = [0.3, 0.7, 1]
HOT_AIR       = [1, 0.2, 0]
LIGHT_OFF     = [0, 0, 0]

def manage_door(sim, message):
    if message == "close":
        sim.setJointTargetPosition(door, 0, [])
    if message == "open":
        sim.setJointTargetPosition(door, -0.9, [])

def manage_main_light(sim, message):

    #color = sim.getObjectColor(main_light,0,COLOR_COMPONENT)
    if message == "on":
        sim.setShapeColor(main_light, None, COLOR_COMPONENT, MAIN_LIGHT_ON)
    if message == "off":
        sim.setShapeColor(main_light, None, COLOR_COMPONENT, LIGHT_OFF)

def manage_air(sim, message):
    if message == "hot_air":
        sim.setShapeColor(air_conditioner_status, None, COLOR_COMPONENT, HOT_AIR)
    if message == "cold_air":
        sim.setShapeColor(air_conditioner_status, None, COLOR_COMPONENT, COLD_AIR)
    if message == "off":
        sim.setShapeColor(air_conditioner_status, None, COLOR_COMPONENT, LIGHT_OFF)



def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        if msg.topic == "door":
            manage_door(sim, msg.payload.decode())
        if msg.topic == "main_light":
            manage_main_light(sim, msg.payload.decode())
        if msg.topic == "air_conditioner":
            manage_air(sim, msg.payload.decode())


    for topic in topics:
        client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
