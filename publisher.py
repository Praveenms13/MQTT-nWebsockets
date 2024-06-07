import paho.mqtt.client as mqtt
import time
import random
from dotenv import load_dotenv
import os
load_dotenv()

mqtt_broker = os.environ.get('MQTT_BROKER')
mqtt_port = int(os.environ.get('MQTT_PORT'))
mqtt_topic = os.environ.get('MQTT_TOPIC')
username = os.environ.get('MQTT_USERNAME')
password = os.environ.get('MQTT_PASSWORD')
client = mqtt.Client(client_id="id1")
client.username_pw_set(username, password)
client.connect(mqtt_broker)

def mqtt_msgsend_cam(data, topic="Simple Chat", qos=0):
    client.publish(topic, data, qos=qos)

words = [
    "lovely", 
    "amazing", 
    "beautiful", 
    "wonderful", 
    "fantastic",
    "awesome",
    "incredible",
    "fabulous",
    "marvelous",
    "terrific",
    "stunning",
    "astonishing",
    "awe-inspiring",
    "extraordinary",
    "unbelievable",
    "remarkable",
    "miraculous"
    ]

try:
    while True:
        word = random.choice(words)
        message_data = f"word=>{word}"
        mqtt_msgsend_cam(message_data)
        print(f"Sent: {message_data}")
        time.sleep(5)
except KeyboardInterrupt:
    client.disconnect()
    print("Publisher stopped")