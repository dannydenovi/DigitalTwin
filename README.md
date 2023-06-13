# DigitalTwin
Progetto di Laboratorio di Reti e Sistemi Distribuiti

## Documentazione

[Coppelia API Python](https://github.com/CoppeliaRobotics/zmqRemoteApi/tree/master/clients/python)

[DHT11](https://github.com/adafruit/Adafruit_Python_DHT)

## Dipendenze

### MQTT e Remote API Coppelia Sim:
```sh
pip install paho-mqtt coppeliasim_zmqremoteapi_client
```

### DHT11 Adafruit:

```sh
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
sudo python setup.py install
```

### Abilitare accesso remoto MQTT:

```sh
sudo apt install mosquitto
sudo systemctl enable mosquitto.service
```
```sh
sudo nano /etc/mosquitto/mosquitto.conf
```

E inserire:
```
listener 1883
allow_anonymous true
```


