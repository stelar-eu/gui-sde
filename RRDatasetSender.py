from messages.Datapoint import Datapoint
from messages.sendDatapoint import SendDatapoint


class RRDatasetSender:
    def __init__(self, data, App):
        self.data = data
        self.App = App

    def send(self):
        # First, we need to skip the first 1-19 lines of the data
        # Then, the rows need to be split by the comma and mapped to a Datapoint object
        # Data is in format [STAID, SOUID, DATE, RR, Q_RR]
        # Finally, the Datapoint object needs to be sent to Kafka
        datasetKey = "RR"
        streamID = "S1"

        for record in self.data[19:30]:
            values = record.split(",")
            staid = values[0]
            souid = values[1]
            date = values[2]
            rr = values[3]
            q_rr = values[4]
            datapoint = SendDatapoint(datasetKey, streamID, {"STAID": staid, "SOUID": souid, "DATE": date, "RR": rr, "Q_RR": q_rr}, self.App)
            # Send the datapoint to Kafka
            datapoint.send_datapoint_to_kafka_topic()
