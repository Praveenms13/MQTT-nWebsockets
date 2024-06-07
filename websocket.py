import asyncio
import websockets
import paho.mqtt.client as mqtt
import http.client
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os

load_dotenv()

mqtt_broker = os.environ.get('MQTT_BROKER')
mqtt_port = int(os.environ.get('MQTT_PORT'))
mqtt_topic = os.environ.get('MQTT_TOPIC')
username = os.environ.get('MQTT_USERNAME')
password = os.environ.get('MQTT_PASSWORD')

websocket_port = 6789

connected_clients = set()

loop = asyncio.get_event_loop()

def on_message(client, userdata, message):
    data = message.payload.decode()
    print(f"Received message '{data}' on topic '{message.topic}'")

    word = data.split("=>")[1].strip()
    synonyms = fetch_synonyms(word)

    message_to_send = f"Word: {word}\nSynonyms: {', '.join(synonyms)}"
    asyncio.run_coroutine_threadsafe(broadcast_message(message_to_send), loop)

def fetch_synonyms(word):
    rapidapi_key = os.environ.get('RAPIDAPI_KEY')
    rapidapi_host = os.environ.get('RAPIDAPI_HOST')

    conn = http.client.HTTPSConnection(rapidapi_host)

    headers = {
        'x-rapidapi-key': rapidapi_key,
        'x-rapidapi-host': rapidapi_host
    }

    conn.request("GET", f"/words/{word}/synonyms", headers=headers)

    res = conn.getresponse()
    data = res.read()

    synonyms = data.decode("utf-8").split(",")
    conn.close()

    return synonyms

async def broadcast_message(message):
    for client in connected_clients:
        try:
            await client.send(message)
        except websockets.exceptions.ConnectionClosed:
            connected_clients.remove(client)

async def websocket_handler(websocket, path):
    connected_clients.add(websocket)
    try:
        await websocket.send("Connected to WebSocket server")
        async for message in websocket:
            await websocket.send(f"You sent: {message}")
    finally:
        connected_clients.remove(websocket)

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username, password)
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, mqtt_port)
mqtt_client.subscribe(mqtt_topic)

async def main():
    async with websockets.serve(websocket_handler, "localhost", websocket_port):
        mqtt_client.loop_start()
        print(f"WebSocket server started on port {websocket_port}")
        await asyncio.Future()  

loop.run_until_complete(main())