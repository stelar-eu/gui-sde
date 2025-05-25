from urllib.parse import urlparse

from messages.Datapoint import Datapoint
import json

from weatherData.MapLocations import MapLocations

from kafka import KafkaProducer

from kafka.errors import KafkaError
import streamlit as st


class DataClientStreamLit:
    def __init__(self, data, name, res):
        self.data = data
        self.dataset_name = name
        self.resource = res
        if "sde_parameters" not in st.session_state:
            st.error("Session state not initialized. Please initialize the session state.")
        self.data_topic = st.session_state.sde_parameters["data_topic"]
        bootstrap_servers = st.session_state.sde_parameters["bootstrap_servers"]

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
            if self.resource.name == "stations_rr":
                return
            self.send_rr(dataSetkey, StreamID)

    def send_rr(self, dataSetkey, StreamID):
        # first get map locations file:
        map_location_filename = "stations_rr"
        ml = MapLocations()
        resources = st.session_state.selected_dataset.resources
        locations = None
        for resource in resources:
            if resource.name == map_location_filename:
                bucket_name, object_path = st.session_state.parse_s3_url(resource.url)
                locations = st.session_state.minio_client.get_object(bucket_name, object_path)
                break
        if locations:
            ml.read_stations(locations)
            ml.print_stats()
        if self.producer is None:
            self.producer = KafkaProducer(**self.conf)

        for record in self.data[19:50]:
            values = record.split(",")
            if len(values) < 5:
                continue
            staid = values[0].replace(' ', '')
            x, y = ml.get_domain(int(staid))
            souid = values[1].replace(' ', '')
            date = values[2].replace(' ', '')
            rr = values[3].replace(' ', '')
            q_rr = values[4].replace(' ', '')
            val = {"x": x, "y": y, "SOUID": souid, "DATE": int(date), "RR": int(rr), "Q_RR": q_rr}
            datapoint = {"dataSetkey": dataSetkey, "streamID": StreamID, "values": val}
            self.producer.send(self.data_topic, value=datapoint, key=dataSetkey)
        self.producer.flush()
        self.producer.close()
    #
    # def parse_s3_url(self, s3_url):
    #     parsed_url = urlparse(s3_url)
    #     bucket_name = parsed_url.netloc  # Extracts 'klms-bucket'
    #     object_path = parsed_url.path.lstrip('/')  # Extracts 'profile.txt'
    #     return bucket_name, object_path
