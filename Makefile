ARCH := $(shell uname -m)

default:
	@make -s install

install:
	@echo "Installing dependencies..."
	@apt update && apt install -y python3-pip git
	@pip3 install paho-mqtt
	@if [ $(ARCH) = "x86_64" ]; then\
		make install_x86;\
	else\
		make install_arm;\
	fi

install_x86:
	@pip3 install coppeliasim_zmqremoteapi_client


install_arm:
	@apt update && apt install -y mosquitto
	@systemctl enable --now mosquitto.service
	@echo listener 1883 | tee -a /etc/mosquitto/mosquitto.conf
	@echo allow_anonymous true | tee -a /etc/mosquitto/mosquitto.conf
	@git clone https://www.github.com/adafruit/Adafruit_Python_DHT.git
	@cd Adafruit_Python_DHT && python3 setup.py install
	@systemctl restart mosquitto.service

