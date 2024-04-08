from confluent_kafka import Producer
import json

from messages.Request import Request


class SendRequest:
#     def __init__(self):
#         self.requestID = 0
#         self.datasetKey = ""
#         self.streamID = ""
#         self.uid = 0
#         self.synID = 0
#         self.noOfP = 0
#         self.parameters = []

    def __init__(self, par, synParameters, App):
        self.requestID = int(par[0])
        self.datasetKey = par[1]
        self.streamID = par[2]
        self.uid = int(par[3])
        self.synID = int(par[4])
        self.noOfP = int(par[5])
        self.parameters = synParameters
        self.App = App

    def __init__(self, requestID, datasetKey, streamID, uid, synID, noOfP, synParameters, App):
        self.requestID = requestID
        self.datasetKey = datasetKey
        self.streamID = streamID
        self.uid = uid
        self.synID = synID
        self.noOfP = noOfP
        self.parameters = synParameters
        self.App = App

    def send_request_to_kafka_topic(self):
        topic_requests = "request_topic"

        bootstrap_servers = "localhost:9092"
        conf = {
            'bootstrap.servers': bootstrap_servers,
        }

        producer = Producer(**conf)

        # Creating a Request object
        request = {
            "key": self.datasetKey,
            "dataSetkey": self.datasetKey,
            "requestID": self.requestID,
            "synopsisID": self.synID,
            "uid": self.uid,
            "streamID": self.streamID,
            "param": self.parameters,
            "noOfP": self.noOfP
        }
        if self.requestID == 1:
            self.App.add_synopsis(request)
        elif self.requestID == 2:
            self.App.delete_synopsis(request)

        rq = Request(self.datasetKey, self.requestID, self.synID, self.uid, self.streamID, self.parameters, self.noOfP)
        # Serializing Request object to JSON
        #request_json = json.dumps(request)

        producer.produce(topic_requests, key=rq.key_to_kafka(), value=rq.to_json())
        producer.flush()
        print("Request sent to Kafka Topic")

    def set_req_parameters(self, parameters):
        self.parameters = parameters


# Usage example:
if __name__ == "__main__":
    # Create a SendRequest object with parameters
    parameters = ["param1", "param2", "param3"]
    send_request = SendRequest([1, "key", "stream", 101, 30, 2], parameters, None)
    #send_request.set_req_parameters(parameters)

    # Send the request to Kafka topic
    send_request.send_request_to_kafka_topic()
    #
    # basic_param = "StockID;price;Queryable;0.002;0.99;4"
    # req = "D2, S2, 101, 30, 2"
    # all_param = "StockID, price, Queryable, StockID;price;Queryable;0.002;0.99;4, 1, -50, 100, 0, 100, 16"
    # cm_par = ["StockID", "price", "Queryable", "0.002", "0.99", "4"]
    # omni_par = ["RID", "price", "Queryable", "4", "0.99", "0.002", "5000", "31", "4"]