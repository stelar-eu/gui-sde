import json

class Datapoint:
    def __init__(self, key="", stream_id="", values=None):
        if values is None:
            values = {}

        self.DataSetkey = key
        self.StreamID = stream_id
        self.values = values

    @classmethod
    def from_json(cls, key, stream_id, json_str):
        values = json.loads(json_str)
        return cls(key, stream_id, values)

    def value_to_kafka(self):
        return f"\"{self.DataSetkey},{self.StreamID},{json.dumps(self.values)}\""

    def key_to_kafka(self):
        return f"\"{self.DataSetkey}\""

    def get_data_set_key(self):
        return self.DataSetkey

    def set_data_set_key(self, key):
        self.DataSetkey = key

    def get_stream_id(self):
        return self.StreamID

    def set_stream_id(self, stream_id):
        self.StreamID = stream_id

    def get_values(self):
        return self.values

    def set_values(self, values):
        self.values = values

    def to_json_string(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return f"Datapoint{{DataSetkey='{self.DataSetkey}', StreamID='{self.StreamID}', values='{self.values}'}}"


# Usage example:
if __name__ == "__main__":
    # Create a Datapoint object
    values = {
        "key1": "value1",
        "key2": "value2"
    }
    datapoint = Datapoint("key", "stream", values)

    # Convert to JSON string
    json_str = datapoint.to_json_string()
    print(json_str)

    # Convert to Kafka value string
    kafka_value = datapoint.value_to_kafka()
    print(kafka_value)

    # Convert to Kafka key string
    kafka_key = datapoint.key_to_kafka()
    print(kafka_key)

    # Creating from JSON
    json_str = '{"DataSetkey": "key", "StreamID": "stream", "values": {"key1": "value1", "key2": "value2"}}'
    new_datapoint = Datapoint.from_json("key", "stream", json_str)
    print(new_datapoint)