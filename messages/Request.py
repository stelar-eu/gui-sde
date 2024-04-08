import json
import ast
class Request:
    def __init__(self, key="", request_id=0, synopsis_id=0, u_id=0, stream_id="", param=None, no_of_p=0):
        if param is None:
            param = ""
        self.key = key
        self.dataSetkey = key
        self.requestID = request_id
        self.synopsisID = synopsis_id
        self.uid = u_id
        self.streamID = stream_id
        self.param = param
        self.noOfP = no_of_p

    @classmethod
    def from_tokens(cls, value_tokens):
        key = value_tokens[0]
        request_id = int(value_tokens[1])
        u_id = int(value_tokens[2])
        synopsis_id = int(value_tokens[3])
        stream_id = value_tokens[4]
        param = value_tokens[5].split(";")
        no_of_p = int(value_tokens[6])
        return cls(key, request_id, synopsis_id, u_id, stream_id, param, no_of_p)

    def to_json(self):
        return json.dumps(self.__dict__, indent=4)

    def to_kafka_producer(self):
        pr = ";".join(self.param)
        return f"\"{self.dataSetkey},{self.requestID},{self.uid},{self.synopsisID},{self.streamID},{pr},{self.noOfP}\""

    def key_to_kafka(self):
        return f"\"{self.dataSetkey}\""

    def to_kafka_json(self):
        return self.to_json().encode()

    def __str__(self):
        return f"Request [key={self.dataSetkey}, RequestID={self.requestID}, SynopsisID={self.synopsisID}, UID={self.uid}, StreamID={self.streamID}, Param={self.param}, NoOfP={self.noOfP}]"

    def to_sum_string(self):
        return f"[{self.uid},{self.synopsisID},{self.param},{self.noOfP}]\n"

    def set_parameters(self, param):
        self.param = param
    def set_data_set_key(self, key):
        self.dataSetkey = key
    def set_request_id(self, request_id):
        self.requestID = request_id
    def set_synopsis_id(self, synopsis_id):
        self.synopsisID = synopsis_id
    def set_uid(self, u_id):
        self.uid = u_id
    def set_stream_id(self, stream_id):
        self.streamID = stream_id
    def set_no_of_p(self, no_of_p):
        self.noOfP = no_of_p

    @classmethod
    def from_string(cls, line):
        print(line)
        return ast.literal_eval(line)
        # tokens = line.split(",")
        # key = tokens[0]
        # request_id = int(tokens[1])
        # u_id = int(tokens[2])
        # synopsis_id = int(tokens[3])
        # stream_id = tokens[4]
        # param = tokens[5].split(";")
        # no_of_p = int(tokens[6])
        # return cls(key, request_id, synopsis_id, u_id, stream_id, param, no_of_p)


# Usage example:
if __name__ == "__main__":
    # Create a Request object
    request = Request("key", 1, 2, 3, "stream", ["param1", "param2"], 5)

    # Convert to JSON
    json_str = request.to_json()
    print(json_str)

    # Convert to Kafka producer string
    kafka_str = request.to_kafka_producer()
    print(kafka_str)

    # Convert to Kafka key string
    kafka_key = request.key_to_kafka()
    print(kafka_key)

    # Convert to Kafka JSON bytes
    kafka_json_bytes = request.to_kafka_json()
    print(kafka_json_bytes.decode())

    # Creating from tokens
    value_tokens = ["key", "1", "3", "2", "stream", "param1;param2", "5"]
    new_request = Request.from_tokens(value_tokens)
    print(new_request)