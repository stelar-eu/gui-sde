from confluent_kafka import Producer
import json

from messages.Datapoint import Datapoint
import hashlib

class SendDatapoint:
    def __init__(self, datasetKey, streamID, values, App):
        self.datasetKey = datasetKey
        self.streamID = streamID
        self.values = values
        self.App = App

    def send_datapoint_to_kafka_topic(self):
        data_topic = self.App.sde_parameters["data_topic"]

        bootstrap_servers = self.App.sde_parameters["bootstrap_servers"]
        conf = {
            'bootstrap.servers': bootstrap_servers,
        }

        producer = Producer(**conf)

        # Creating a Request object
        datapoint = {
            "dataSetkey": self.datasetKey,
            "streamID": self.streamID,
            "values": self.values,
        }

        dp = Datapoint(self.datasetKey, self.streamID, self.values)

        # Serializing Request object to JSON
        #request_json = json.dumps(request)
        print(f"Datapoint: {dp}")
        producer.produce(data_topic, key=dp.key_to_kafka(), value=dp.to_json())
        producer.flush()

        # print("Request sent to Kafka Topic")

