import json
import threading
from tkinter import messagebox

import customtkinter
from confluent_kafka import *
from ScrollableRadioButtonFrame import ScrollableRadiobuttonFrame
from messages.sendRequest import SendRequest

from messages.sendRequest import SendRequest


class QueryNormal:
    frame = None

    def __init__(self, App):
        # Current synopsis
        self.curUID = None
        self.curStreamID = None
        self.curDatasetKey = None
        self.curSynopsisID = None
        self.curNoOfP = None
        self.curParameters = None

        self.scrollable_frame = None
        self.App = App
        self.output = None
        self.frame = None
        self.labels = ["Estimate:"]
        self.entry_widgets = {}

        self.queries = {}

        self.queryID = 0

    def set_query_parameters(self):
        self.setCurSynopsis(self.scrollable_frame.get_checked_item())


        # request class with textboxes for datasetkey, streamID, UID, SynopsisID, NoOfP and parameters
        dataEntry = customtkinter.CTkFrame(self.frame, width=200, height=250, fg_color="#000811")

        dataEntry.grid(row=2, columnspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        label_dataEntry = customtkinter.CTkLabel(dataEntry, text="Step 2: Choose Query Parameters",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        label_dataEntry.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.queryParameters = customtkinter.CTkEntry(master=dataEntry, width=250, placeholder_text="Query Parameters")
        self.queryParameters.grid(row=1, column=0, padx=20, pady=(10, 10))


        # create a button to send the request to the kafka topic
        bt_query_synopsis = customtkinter.CTkButton(master=dataEntry, text="Submit Query", command=self.send_request)
        bt_query_synopsis.grid(row=1, column=1, padx=(20, 0), pady=(20, 20))

    def set_frame3(self):
        self.frame = self.App.frames["frame3"]
        # set title
        title = customtkinter.CTkLabel(self.frame, text="Query Synopsis",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        title.place(relx=0.5, rely=0.02, anchor=customtkinter.CENTER)
        self.create_existing_synopsis_frame()
        self.create_widgets()


        self.App.frames["frame3"] = self.frame

    def send_request(self):

        # 3 because requestId 3 is querying a synopsis.
        splitQueryParameters = self.queryParameters.get().split(", ")

        rq = SendRequest(3, self.curDatasetKey, self.curStreamID, self.curUID, self.curSynopsisID,
                         self.curNoOfP, splitQueryParameters, self.App)

        rq.send_request_to_kafka_topic()
        self.queries[self.queryID] = {"parameters": splitQueryParameters, "estimate": None}

        self.queryID += 1
        messagebox.showinfo("Request Sent", "Request sent to Kafka Topic", parent=self.frame)

    def create_widgets(self):

        #self.output = customtkinter.CTkFrame(self.frame, width=250, height=250, fg_color="#000811")

        self.output = customtkinter.CTkFrame(self.frame, width=500, height=250, fg_color="#000811")
        #self.output.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        label_output = customtkinter.CTkLabel(self.output, text="Query Output",
                                              font=customtkinter.CTkFont(size=15, weight="bold"))
        label_output.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.output.place(relx=0.75, rely=0.25, anchor=customtkinter.CENTER)

        # grid for
        for i, label_text in enumerate(self.labels):
            label = customtkinter.CTkLabel(self.output, text=label_text, font=customtkinter.CTkFont(size=14))
            label.grid(row=i + 1, column=0, padx=20, pady=(10, 10))

            self.entry_widgets[label_text] = customtkinter.CTkTextbox(self.output,width=500, height=250,
                                                                       font=customtkinter.CTkFont(size=14))
            # self.entry_widgets[label_text] = customtkinter.CTkScrollableFrame(self.output, width=250, height=250)
            self.entry_widgets[label_text].grid(row=i + 1, column=1, padx=20, pady=(10, 10))

        self.start_kafka_consumer()

    def start_kafka_consumer(self):
        def consume_messages():

            queryCounter = 0
            props = {
                'bootstrap.servers': 'localhost:9092',
                'group.id': 'OUT',
            }

            consumer = Consumer(props)

            try:
                consumer.subscribe(['OUT'])

                while True:
                    msg = consumer.poll()
                    if msg is None:
                        continue
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            # End of partition, ignore
                            continue
                        else:
                            raise KafkaException(msg.error())

                    message = msg.value().decode('utf-8')

                    m = json.loads(message)
                    print(m)
                    estimate = m["estimation"]
                    print("Received message: {}".format(estimate))
                    self.queries[queryCounter]["estimate"] = estimate
                    self.entry_widgets["Estimate:"].insert(customtkinter.END, "\n" + "Query " + str(queryCounter) +
                                                           " with parameters: " +
                                                           str(self.queries[queryCounter]["parameters"]) +
                                                           " | estimate: " + str(estimate))

                    self.entry_widgets["Estimate:"].see(customtkinter.END)
                    queryCounter += 1

            except KeyboardInterrupt:
                pass
            finally:
                consumer.close()

        # Create a thread to run the Kafka consumer
        kafka_thread = threading.Thread(target=consume_messages)
        kafka_thread.daemon = True
        kafka_thread.start()

    def create_existing_synopsis_frame(self):
        self.button_load_synopses = customtkinter.CTkButton(self.frame,
                                                            text="Start Querying Synopses",
                                                            command=self.load_existing_synopses,
                                                            anchor="CENTER")
        self.button_load_synopses.grid(row=0, column=0, padx=(20, 0), pady=(50, 0))

    def reload_existing_synopses(self):
        if self.scrollable_frame is not None:
            self.scrollable_frame.delete_all_items()
        for syn in self.App.existing_synopses:
            if self.App.existing_synopses[syn]["synopsisID"] != "30": #Spatial sketches in other frame
                self.scrollable_frame.add_item(self.App.existing_synopses[syn])
            #
            # "uid: {} | synID: {} | Dataset: {} | StreamID: {} | NoOfP: {} | Parameters: {}".format(
            #                                           self.App.existing_synopses[syn]['uid'],
            #                                           self.App.existing_synopses[syn]['synopsisID'],
            #                                           self.App.existing_synopses[syn]['dataSetkey'],
            #                                           self.App.existing_synopses[syn]['streamID'],
            #                                           self.App.existing_synopses[syn]['noOfP'],
            #                                           self.App.existing_synopses[syn]['param']))

    def load_existing_synopses(self):
        self.button_load_synopses.destroy()
        self.button_load_synopses = customtkinter.CTkButton(self.frame,
                                                            text="Reload Synopses",
                                                            command=self.reload_existing_synopses)
        self.button_load_synopses.grid(row=0, column=0, padx=(20, 0), pady=(50, 0))
        self.scrollable_frame_synopses = []
        self.App.read_syns_from_file()





        self.scrollable_frame = ScrollableRadiobuttonFrame(master=self.frame, item_list=self.scrollable_frame_synopses,
                                                           command=self.set_query_parameters,
                                                           label_text="Step 1: Load Existing Synopses", width=650,
                                                                 height=400, fg_color="#000811")
        self.scrollable_frame.grid(row=1, columnspan=4, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.reload_existing_synopses()

    def setCurSynopsis(self, syn):
        print(syn)
        self.curDatasetKey = syn['dataSetkey']
        self.curStreamID = syn['streamID']
        self.curUID = syn['uid']
        self.curSynopsisID = syn['synopsisID']
        self.curNoOfP = syn['noOfP']
        self.curParameters = syn['param']

