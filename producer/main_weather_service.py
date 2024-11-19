import time

import requests
from grid import grid_point
from flask import Flask
from confluent_kafka import Producer

app = Flask(__name__)

WEATHER_API_URL = 'https://api.weather.gov/gridpoints/{gridId}/{gridX},{gridY}/forecast'

@app.route('/weather', methods=['GET'])
def get_weather():
    grid_id, grid_x, grid_y = grid_point.get_gridData()
    response = requests.get(WEATHER_API_URL.format(gridId=grid_id, gridX=grid_x, gridY=grid_y))
    response.raise_for_status()
    return response.json().get('properties')['periods'][0]

def kafka_producer():
    kafka_broker = 'kafka:9092'
    producer = Producer({'bootstrap.servers':kafka_broker})

    topic = "weather_topic"

    while True:
        weather_data = get_weather()
        if weather_data:
            message = str(weather_data)
            try:
                producer.produce(topic, value=message)
                producer.flush()
                print(f"Produced: {message}")
            except Exception as e:
                print(f"Error producingmessage: {e}")
        time.sleep(30)

if __name__ == '__main__':
    kafka_producer()
    # app.run(host='0.0.0.0', debug=True, port=3000)
