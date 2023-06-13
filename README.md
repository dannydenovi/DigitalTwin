# DigitalTwin
Progetto di Laboratorio di Reti e Sistemi Distribuiti

## Installazione

 - Clonare la repo: `git clone https://github.com/dannydenovi/DigitalTwin.git`
 - Spostarsi nella cartella: `cd /path/to/DigitalTwin`
 - (Opzionale) Creare un ambiente virtuale: `python3 -m venv venv` ed in seguito `source venv/bin/activate`
 - Installare le dipendenze con `python3 setup.py install`


## Funzionamento

### Raspberry Pi

(TODO: SCRIVERE I PIN)

 - Eseguire `python3 home.py`
 
 #### Flags
 
 - `-r/--random`: Nel caso in cui si volessero generare numeri random per la temperatura e disattivare il sensore.

### MacOS/Linux

- Aprire con CoppeliaSim `room.ttt`
- Eseguire `python3 simulation.py`


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


