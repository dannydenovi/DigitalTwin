from setuptools import setup, find_packages
import platform
import subprocess

dependencies = [
    'paho-mqtt',
]

# Controlla l'architettura e aggiungi la dipendenza se necessario
if platform.machine() == 'x86_64':
    dependencies.append('coppeliasim_zmqremoteapi_client')

# Esegui comandi specifici per Raspberry Pi
if platform.machine().startswith('arm') and platform.system() == 'Linux':
    subprocess.run(['sudo', 'apt', 'install', 'mosquitto'])
    subprocess.run(['sudo', 'systemctl', 'enable', 'mosquitto.service'])
    subprocess.run(['echo', 'listener 1883 | sudo tee -a /etc/mosquitto/mosquitto.conf'])
    subprocess.run(['echo', 'allow_anonymous true | sudo tee -a /etc/mosquitto/mosquitto.conf'])
    subprocess.run(['git', 'clone', 'https://github.com/adafruit/Adafruit_Python_DHT.git'])
    subprocess.run(['cd', 'Adafruit_Python_DHT', '&&', 'sudo', 'python', 'setup.py', 'install'])

setup(
    name='DigitalTwin',
    version='1.0.0',
    packages=find_packages(),
    install_requires=dependencies,
)
