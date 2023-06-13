.PHONY: install

ARCH := $(shell arch)

install:
    # Installazione solo su Raspberry Pi
    ifeq ($(ARCH), aarch64)
        sudo apt install mosquitto
        sudo systemctl enable mosquitto.service
        echo "listener 1883" | sudo tee -a /etc/mosquitto/mosquitto.conf
        echo "allow_anonymous true" | sudo tee -a /etc/mosquitto/mosquitto.conf
        git clone https://github.com/adafruit/Adafruit_Python_DHT.git
        cd Adafruit_Python_DHT && sudo python setup.py install
    endif

    # Installazione di coppeliasim solo su architettura diversa da aarch64
    ifneq ($(ARCH), aarch64)
        pip install coppeliasim_zmqremoteapi_client
    endif
    
    # Installazione di paho-mqtt indipendentemente dall'architettura
    pip install paho-mqtt
    
    
