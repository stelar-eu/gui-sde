from messages.Datapoint import Datapoint
import json

from kafka import KafkaProducer
from kafka.errors import KafkaError

class DataClient:
    def __init__(self, data, App, name):
        self.data = data
        self.dataset_name = name
        self.App = App
        self.data_topic = self.App.sde_parameters["data_topic"]

        bootstrap_servers = self.App.sde_parameters["bootstrap_servers"]
        self.conf = {
            'bootstrap_servers': bootstrap_servers,
            'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
            'key_serializer': lambda v: json.dumps(v).encode('utf-8')
        }

        self.producer = KafkaProducer(**self.conf)

    def send(self, dataSetkey, StreamID):
        # First, we need to skip the first 1-19 lines of the data
        # Then, the rows need to be split by the comma and mapped to a Datapoint object
        # Data is in format [STAID, SOUID, DATE, RR, Q_RR]
        # Finally, the Datapoint object needs to be sent to Kafka

        dataSetkey = dataSetkey
        StreamID = StreamID
        if self.dataset_name == "synopses_experiment":
            self.send_rr(dataSetkey, StreamID)

    def send_rr(self, dataSetkey, StreamID):
        if self.producer is None:
            self.producer = KafkaProducer(**self.conf)

        for record in self.data[19:50]:
            values = record.split(",")
            if len(values) < 5:
                continue
            staid = values[0].replace(' ', '')
            souid = values[1].replace(' ', '')
            date = values[2].replace(' ', '')
            rr = values[3].replace(' ', '')
            q_rr = values[4].replace(' ', '')
            val = {"STAID": staid, "SOUID": souid, "DATE": int(date), "RR": int(rr), "Q_RR": q_rr}
            datapoint = {"dataSetkey": dataSetkey, "streamID": StreamID, "values": val}
            print(datapoint)
            self.producer.send(self.data_topic, value=datapoint, key=dataSetkey)
        self.producer.flush()
        self.producer.close()
