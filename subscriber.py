import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv()

mqtt_broker = os.environ.get('MQTT_BROKER')
mqtt_port = int(os.environ.get('MQTT_PORT'))
mqtt_topic = os.environ.get('MQTT_TOPIC')
username = os.environ.get('MQTT_USERNAME')
password = os.environ.get('MQTT_PASSWORD')

def on_message(client, userdata, message):
    print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")

client = mqtt.Client()
client.username_pw_set(username, password)

client.on_message = on_message
client.connect(mqtt_broker, mqtt_port)
client.subscribe(mqtt_topic)

try:
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()
    print("Subscriber stopped")
