
import tkinter as tk
import customtkinter
import json
import os
from PIL import Image, ImageTk, ImageOps

from CustomCTkTable import *
import threading
from tkinter import messagebox, ttk

from ScrollableRadioButtonFrame import ScrollableRadiobuttonFrame
class QueryNormal:
    frame = None

    def __init__(self, App):
        # App
        self.dataEntry = None
        self.current_synopsis = None
        self.num_queries = None
        self.output_table = None
        self.dataset_entry = None
        self.dataset = None
        self.App = App

        # Current synopsis

        # Widgets
        self.button_load_synopses = None
        self.scrollable_frame_synopses = None

        self.scrollable_frame = None
        self.output = None
        self.frame = None
        self.labels = ["Estimate:"]
        self.entry_widgets = {}


        self.selected_cells = []

        # Current synopsis
        self.curExternalUID = None
        self.curUID = None
        self.curStreamID = None
        self.curDatasetKey = None
        self.curSynopsisID = None
        self.curNoOfP = None
        self.curParameters = None


        self.curMaxCol = None
        self.curMinCol = None
        self.curMaxRow = None
        self.curMinRow = None

    def set_query_parameters(self):
        self.current_synopsis = self.scrollable_frame.get_checked_item()
        # self.setCurSynopsis(self.scrollable_frame.get_checked_item())
        self.dataEntry = customtkinter.CTkFrame(self.frame, width=200, height=250, fg_color="#000811")

        self.dataEntry.grid(row=2, columnspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        label_dataEntry = customtkinter.CTkLabel(self.dataEntry, text="Step 2: Choose Query Parameters",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        label_dataEntry.grid(row=0, columnspan=4, padx=20, pady=(10, 10), sticky="nsew")

        if self.App.current_synopses is None:
            label = customtkinter.CTkLabel(self.dataEntry, text="Custom Parameters",
                                           font=customtkinter.CTkFont(size=14))
            label.grid(row=1, column=0, padx=20, pady=(10, 10))
            entry = customtkinter.CTkEntry(master=self.dataEntry, width=250, placeholder_text="Query Parameters")
            entry.grid(row=1, column=1, padx=20, pady=(10, 10))
        else:
            for i, label_text in enumerate(self.current_synopsis["param"]):
                label = customtkinter.CTkLabel(self.dataEntry, text=label_text,
                                               font=customtkinter.CTkFont(size=14))
                label.grid(row=i + 1, column=0, padx=20, pady=(10, 10))
                entry = customtkinter.CTkEntry(master=self.dataEntry, width=250, placeholder_text=label_text)
                entry.grid(row=i + 1, column=1, padx=20, pady=(10, 10))
        self.dataEntry.get = lambda: ", ".join([e.get() for e in self.dataEntry.winfo_children() if isinstance(e, customtkinter.CTkEntry)])

        # create a button to send the request to the kafka topic
        bt_query_synopsis = customtkinter.CTkButton(master=self.frame, text="Submit Query",
                                                    command=self.send_request)
        bt_query_synopsis.grid(row=3, columnspan=2, padx=(20, 0), pady=(20, 20))

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
        print("data entry is: ", self.dataEntry.get())
        basicSketchQueryParameters = self.dataEntry.get().replace(" ", "").split(",")# + "1".split(",")
        queryParameters = [None] * len(basicSketchQueryParameters)
        for i, v in enumerate(basicSketchQueryParameters):
            queryParameters[i] = v

        rq_data = {
            "key": self.current_synopsis["dataSetkey"],
            "streamID": self.current_synopsis["StreamID"],
            "synopsisID": self.current_synopsis["synopsisID"],
            "requestID": 3,
            "dataSetkey": self.current_synopsis["dataSetkey"],
            "param": queryParameters,
            "noOfP": self.current_synopsis["noOfP"],
            "uid": self.current_synopsis["uid"],
            "externalUID": "Estimate:" + str(self.current_synopsis["uid"])
        }
        output = self.App.sde.send_request(rq_data, "Estimate:" + str(self.current_synopsis["uid"]))

        self.add_estimate_row(output)

        # small timeout
        messagebox.showinfo("Query Successful", "Query successfully submitted.", parent=self.frame)

    def create_widgets(self):
        if self.output:
            self.output.destroy()

        self.output = customtkinter.CTkFrame(self.frame, width=500, height=250, fg_color="#000811")
        label_output = customtkinter.CTkLabel(self.output, text="Query Output",
                                              font=customtkinter.CTkFont(size=15, weight="bold"))
        label_output.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.output.place(relx=0.75, rely=0.25, anchor=customtkinter.CENTER)

        # grid for
        est_label = customtkinter.CTkLabel(self.output, text="Result", font = customtkinter.CTkFont(size=14))
        est_label.grid(row=1, column=0, padx=20, pady=(10, 10))
        uid_label = customtkinter.CTkLabel(self.output, text="UID", font = customtkinter.CTkFont(size=14))
        uid_label.grid(row=1, column=1, padx=20, pady=(10, 10))
        syn_label = customtkinter.CTkLabel(self.output, text="Synopsis Type", font = customtkinter.CTkFont(size=14))
        syn_label.grid(row=1, column=2, padx=20, pady=(10, 10))
        dataset_label = customtkinter.CTkLabel(self.output, text="Dataset", font = customtkinter.CTkFont(size=14))
        dataset_label.grid(row=1, column=3, padx=20, pady=(10, 10))
        stream_label = customtkinter.CTkLabel(self.output, text="Stream ID", font = customtkinter.CTkFont(size=14))
        stream_label.grid(row=1, column=4, padx=20, pady=(10, 10))
        noOfP_label = customtkinter.CTkLabel(self.output, text="No of P", font = customtkinter.CTkFont(size=14))
        noOfP_label.grid(row=1, column=5, padx=20, pady=(10, 10))
        param_label = customtkinter.CTkLabel(self.output, text="Parameters", font = customtkinter.CTkFont(size=14))
        param_label.grid(row=1, column=6, padx=20, pady=(10, 10))
        self.num_queries = 0

    def create_existing_synopsis_frame(self):
        label_dataset = customtkinter.CTkLabel(self.frame, text="Dataset",
                                               font=customtkinter.CTkFont(size=13, weight="bold"))
        label_dataset.grid(row=0, column=1, padx=(20, 0), pady=(50, 0))
        dataset_text = customtkinter.StringVar(value=self.App.selected_dataset.name)
        self.dataset_entry= customtkinter.CTkEntry(self.frame, placeholder_text="2", textvariable=dataset_text)
        self.dataset_entry.grid(row=0, column=2, padx=(0, 20), pady=(50, 0))

        self.button_load_synopses = customtkinter.CTkButton(self.frame,
                                                            text="Start Querying Synopses",
                                                            command=self.load_existing_synopses,
                                                            anchor="CENTER")
        self.button_load_synopses.grid(row=0, column=0, padx=(20, 0), pady=(50, 0))

    def reload_existing_synopses(self):
        if self.scrollable_frame is not None:
            self.scrollable_frame.delete_all_items()

        self.App.read_syns_from_sde(self.dataset_entry.get())

        self.scrollable_frame = ScrollableRadiobuttonFrame(master=self.frame,
                                                           item_list=self.App.existing_synopses,
                                                           command=self.set_query_parameters,
                                                           label_text="Step 1: Load Existing Synopses", width=650,
                                                           height=400, fg_color="#000811")
        self.scrollable_frame.grid(row=1, columnspan=4, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

    def load_existing_synopses(self):
        self.button_load_synopses.destroy()
        self.button_load_synopses = customtkinter.CTkButton(self.frame,
                                                            text="Reload Synopses",
                                                            command=self.reload_existing_synopses)
        self.button_load_synopses.grid(row=0, column=0, padx=(20, 0), pady=(50, 0))

        self.App.read_syns_from_sde(self.dataset_entry.get())

        self.scrollable_frame = ScrollableRadiobuttonFrame(master=self.frame,
                                                           item_list=self.App.existing_synopses,
                                                           command=self.set_query_parameters,
                                                           label_text="Step 1: Load Existing Synopses", width=650,
                                                           height=400, fg_color="#000811")
        self.scrollable_frame.grid(row=1, columnspan=4, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

    def add_estimate_row(self, output):
        self.num_queries += 1
        est = customtkinter.CTkLabel(self.output, text=output["estimation"], font = customtkinter.CTkFont(size=14))
        est.grid(row=self.num_queries + 1, column=0, padx=20, pady=(10, 10))
        uid = customtkinter.CTkLabel(self.output, text=output["uid"], font = customtkinter.CTkFont(size=14))
        uid.grid(row=self.num_queries + 1, column=1, padx=20, pady=(10, 10))
        syn = customtkinter.CTkLabel(self.output, text=output["synopsisID"], font = customtkinter.CTkFont(size=14))
        syn.grid(row=self.num_queries + 1, column=2, padx=20, pady=(10, 10))
        dataset = customtkinter.CTkLabel(self.output, text=output["key"], font = customtkinter.CTkFont(size=14))
        dataset.grid(row=self.num_queries + 1, column=3, padx=20, pady=(10, 10))
        stream = customtkinter.CTkLabel(self.output, text=output["streamID"], font = customtkinter.CTkFont(size=14))
        stream.grid(row=self.num_queries + 1, column=4, padx=20, pady=(10, 10))
        noOfP = customtkinter.CTkLabel(self.output, text=output["noOfP"], font = customtkinter.CTkFont(size=14))
        noOfP.grid(row=self.num_queries + 1, column=5, padx=20, pady=(10, 10))
        param = customtkinter.CTkLabel(self.output, text=output["param"], font = customtkinter.CTkFont(size=14))
        param.grid(row=self.num_queries + 1, column=6, padx=20, pady=(10, 10))


# import json
# import threading
# from tkinter import messagebox
#
# import customtkinter
# from confluent_kafka import *
# from ScrollableRadioButtonFrame import ScrollableRadiobuttonFrame
# from messages.sendRequest import SendRequest
#
# from messages.sendRequest import SendRequest
#
#
# class QueryNormal:
#     frame = None
#
#     def __init__(self, App):
#         # Current synopsis
#         self.curUID = None
#         self.curStreamID = None
#         self.curDatasetKey = None
#         self.curSynopsisID = None
#         self.curNoOfP = None
#         self.curParameters = None
#
#         self.scrollable_frame = None
#         self.App = App
#         self.output = None
#         self.frame = None
#         self.labels = ["Estimate:"]
#         self.entry_widgets = {}
#
#         self.queries = {}
#
#         self.queryID = 0
#
#     def set_query_parameters(self):
#         self.setCurSynopsis(self.scrollable_frame.get_checked_item())
#
#
#         # request class with textboxes for datasetkey, streamID, UID, SynopsisID, NoOfP and parameters
#         dataEntry = customtkinter.CTkFrame(self.frame, width=200, height=250, fg_color="#000811")
#
#         dataEntry.grid(row=2, columnspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
#         label_dataEntry = customtkinter.CTkLabel(dataEntry, text="Step 2: Choose Query Parameters",
#                                                  font=customtkinter.CTkFont(size=15, weight="bold"))
#         label_dataEntry.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
#         self.queryParameters = customtkinter.CTkEntry(master=dataEntry, width=250, placeholder_text="Query Parameters")
#         self.queryParameters.grid(row=1, column=0, padx=20, pady=(10, 10))
#
#
#         # create a button to send the request to the kafka topic
#         bt_query_synopsis = customtkinter.CTkButton(master=dataEntry, text="Submit Query", command=self.send_request)
#         bt_query_synopsis.grid(row=1, column=1, padx=(20, 0), pady=(20, 20))
#
#     def set_frame3(self):
#         self.frame = self.App.frames["frame3"]
#         # set title
#         title = customtkinter.CTkLabel(self.frame, text="Query Synopsis",
#                                        font=customtkinter.CTkFont(size=20, weight="bold"))
#         title.place(relx=0.5, rely=0.02, anchor=customtkinter.CENTER)
#         self.create_existing_synopsis_frame()
#         self.create_widgets()
#
#
#         self.App.frames["frame3"] = self.frame
#
#     def send_request(self):
#
#         # 3 because requestId 3 is querying a synopsis.
#         splitQueryParameters = self.queryParameters.get().split(", ")
#
#         rq = SendRequest(3, self.curDatasetKey, self.curStreamID, self.curUID, self.curSynopsisID,
#                          self.curNoOfP, splitQueryParameters, self.App)
#
#         rq.send_request_to_kafka_topic()
#         self.queries[self.queryID] = {"parameters": splitQueryParameters, "estimate": None}
#             #.append(self.queryID, {"parameters": splitQueryParameters, "estimate": None})
#
#         self.queryID += 1
#         print("queries after reuqest sent", self.queries)
#         messagebox.showinfo("Request Sent", "Request sent to Kafka Topic", parent=self.frame)
#
#     def create_widgets(self):
#
#         #self.output = customtkinter.CTkFrame(self.frame, width=250, height=250, fg_color="#000811")
#
#         self.output = customtkinter.CTkFrame(self.frame, width=500, height=250, fg_color="#000811")
#         #self.output.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
#         label_output = customtkinter.CTkLabel(self.output, text="Query Output",
#                                               font=customtkinter.CTkFont(size=15, weight="bold"))
#         label_output.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
#         self.output.place(relx=0.75, rely=0.25, anchor=customtkinter.CENTER)
#
#         # grid for
#         for i, label_text in enumerate(self.labels):
#             label = customtkinter.CTkLabel(self.output, text=label_text, font=customtkinter.CTkFont(size=14))
#             label.grid(row=i + 1, column=0, padx=20, pady=(10, 10))
#
#             self.entry_widgets[label_text] = customtkinter.CTkTextbox(self.output,width=500, height=250,
#                                                                        font=customtkinter.CTkFont(size=14))
#             # self.entry_widgets[label_text] = customtkinter.CTkScrollableFrame(self.output, width=250, height=250)
#             self.entry_widgets[label_text].grid(row=i + 1, column=1, padx=20, pady=(10, 10))
#
#         self.start_kafka_consumer()
#
#     def start_kafka_consumer(self):
#         def consume_messages():
#
#             queryCounter = 0
#             props = {
#                 'bootstrap.servers': 'localhost:9092',
#                 'group.id': 'OUT',
#             }
#
#             consumer = Consumer(props)
#
#             try:
#                 consumer.subscribe(['OUT'])
#
#                 while True:
#                     msg = consumer.poll()
#                     if msg is None:
#                         continue
#                     if msg.error():
#                         if msg.error().code() == KafkaError._PARTITION_EOF:
#                             # End of partition, ignore
#                             continue
#                         else:
#                             raise KafkaException(msg.error())
#
#                     message = msg.value().decode('utf-8')
#
#                     m = json.loads(message)
#                     if m['synopsisID'] == 30:
#                         continue
#                     estimate = m["estimation"]
#                     self.entry_widgets["Estimate:"].insert(customtkinter.END, "\n" + "Query " + str(queryCounter) +
#                                                            " with parameters: " +
#                                                            str(self.queries[queryCounter]["parameters"]) +
#                                                            " | estimate: " + str(estimate))
#
#                     self.entry_widgets["Estimate:"].see(customtkinter.END)
#                     queryCounter += 1
#
#             except KeyboardInterrupt:
#                 pass
#             finally:
#                 consumer.close()
#
#         # Create a thread to run the Kafka consumer
#         kafka_thread = threading.Thread(target=consume_messages)
#         kafka_thread.daemon = True
#         kafka_thread.start()
#
#     def create_existing_synopsis_frame(self):
#         self.button_load_synopses = customtkinter.CTkButton(self.frame,
#                                                             text="Start Querying Synopses",
#                                                             command=self.load_existing_synopses,
#                                                             anchor="CENTER")
#         self.button_load_synopses.grid(row=0, column=0, padx=(20, 0), pady=(50, 0))
#
#     def reload_existing_synopses(self):
#         if self.scrollable_frame is not None:
#             self.scrollable_frame.delete_all_items()
#         for syn in self.App.existing_synopses:
#             if self.App.existing_synopses[syn]["synopsisID"] != "30": #Spatial sketches in other frame
#                 self.scrollable_frame.add_item(self.App.existing_synopses[syn])
#             #
#             # "uid: {} | synID: {} | Dataset: {} | StreamID: {} | NoOfP: {} | Parameters: {}".format(
#             #                                           self.App.existing_synopses[syn]['uid'],
#             #                                           self.App.existing_synopses[syn]['synopsisID'],
#             #                                           self.App.existing_synopses[syn]['dataSetkey'],
#             #                                           self.App.existing_synopses[syn]['streamID'],
#             #                                           self.App.existing_synopses[syn]['noOfP'],
#             #                                           self.App.existing_synopses[syn]['param']))
#
#     def load_existing_synopses(self):
#         self.button_load_synopses.destroy()
#         self.button_load_synopses = customtkinter.CTkButton(self.frame,
#                                                             text="Reload Synopses",
#                                                             command=self.reload_existing_synopses)
#         self.button_load_synopses.grid(row=0, column=0, padx=(20, 0), pady=(50, 0))
#         self.scrollable_frame_synopses = []
#         self.App.read_syns_from_file()
#
#
#
#
#
#         self.scrollable_frame = ScrollableRadiobuttonFrame(master=self.frame, item_list=self.scrollable_frame_synopses,
#                                                            command=self.set_query_parameters,
#                                                            label_text="Step 1: Load Existing Synopses", width=650,
#                                                                  height=400, fg_color="#000811")
#         self.scrollable_frame.grid(row=1, columnspan=4, padx=(20, 0), pady=(20, 20), sticky="nsew")
#         self.scrollable_frame.grid_columnconfigure(0, weight=1)
#
#         self.reload_existing_synopses()
#
#     def setCurSynopsis(self, syn):
#         print(syn)
#         self.curDatasetKey = syn['dataSetkey']
#         self.curStreamID = syn['streamID']
#         self.curUID = syn['uid']
#         self.curSynopsisID = syn['synopsisID']
#         self.curNoOfP = syn['noOfP']
#         self.curParameters = syn['param']
#
