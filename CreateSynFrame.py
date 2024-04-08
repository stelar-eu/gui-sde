
from tkinter import messagebox

import customtkinter
from messages.sendRequest import SendRequest
from synMap import SynMap


class CreateSynFrame:
    main_container = None
    frame = None

    datasetKey = None
    streamID = None
    UID = None
    SynopsisID = None
    NoOfP = None
    parameters = None

    def __init__(self, App):
        self.basicSketchSynId = None
        self.App = App
        self.synMap = SynMap.getSynMap(SynMap())

        # copy synopsis frame
        self.frame = self.App.frames["frame2"]

    def set_frame2(self):
        # set title
        title = customtkinter.CTkLabel(self.frame, text="Create Synopsis",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        title.place(relx=0.5, rely=0.02, anchor=customtkinter.CENTER)

        # make Request class with textboxes for datasetkey, streamID, UID, SynopsisID, NoOfP and parameters

        dataEntry = customtkinter.CTkFrame(self.frame, width=250, height=250, fg_color="#000811")

        dataEntry.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        label_dataEntry = customtkinter.CTkLabel(dataEntry, text="Synopsis Parameters",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        label_dataEntry.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")

        label_datasetKey = customtkinter.CTkLabel(dataEntry, text="DatasetKey")
        label_datasetKey.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="n")
        self.datasetKey = customtkinter.CTkEntry(master=dataEntry, placeholder_text="DatasetKey")
        self.datasetKey.grid(row=1, column=1, padx=20, pady=(10, 10), sticky="n")

        label_streamID = customtkinter.CTkLabel(dataEntry, text="StreamID")
        label_streamID.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.streamID = customtkinter.CTkEntry(master=dataEntry, placeholder_text="StreamID")
        self.streamID.grid(row=2, column=1, padx=20, pady=(10, 10))

        label_UID = customtkinter.CTkLabel(dataEntry, text="UID")
        label_UID.grid(row=3, column=0, padx=20, pady=(10, 10))
        self.UID = customtkinter.CTkEntry(master=dataEntry, placeholder_text="UID")
        self.UID.grid(row=3, column=1, padx=20, pady=(10, 10))

        label_SynopsisID = customtkinter.CTkLabel(dataEntry, text="SynopsisID")
        label_SynopsisID.grid(row=4, column=0, padx=20, pady=(10, 10))
        self.SynopsisID = customtkinter.CTkEntry(master=dataEntry, placeholder_text="SynopsisID")
        self.SynopsisID.grid(row=4, column=1, padx=20, pady=(10, 10))

        label_NoOfP = customtkinter.CTkLabel(dataEntry, text="NoOfP")
        label_NoOfP.grid(row=5, column=0, padx=20, pady=(10, 10))
        self.NoOfP = customtkinter.CTkEntry(master=dataEntry, placeholder_text="NoOfP")
        self.NoOfP.grid(row=5, column=1, padx=20, pady=(10, 10))

        dataEntry.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # create a button to send the request to the kafka topic
        bt_create_synopsis = customtkinter.CTkButton(dataEntry, text="Step 1: Choose Dataset + Synopsis Type", height=50,
                                                     command=self.choose_parameters)
        bt_create_synopsis.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.App.frames["frame2"] = self.frame

    def choose_parameters(self):
        synID = self.SynopsisID.get()

        if self.SynopsisID.get() == "" or self.datasetKey.get() == "" or self.streamID.get() == "" or self.UID.get() == "" or self.NoOfP.get() == "":
            messagebox.showerror("Error", "Please fill in all fields", parent=self.frame)
            return
        if synID not in self.synMap:
            messagebox.showerror("Error", "Invalid Synopsis ID", parent=self.frame)
            return
        if self.UID.get() in self.App.existing_synopses:
            messagebox.showerror("Error", "UID {} already exists".format(self.UID.get()), parent=self.frame)
            return



        if synID == "30":
            self.choose_basic_sketch()
        else:
            if synID in self.synMap:
                self.custom_parameters(self.synMap[synID])
            else:
                self.parameters = customtkinter.CTkEntry(master=self.frame, width=250, placeholder_text="Parameters")
                self.parameters.grid(row=1, column=0, padx=20, pady=(10, 10))

            bt_create_synopsis = customtkinter.CTkButton(self.frame, text="Step 2: Choose synopsis specific parameters",
                                                         height=50, command=self.send_request)
            bt_create_synopsis.grid(row=2, column=0, padx=20, pady=(10, 10))


    def choose_basic_sketch(self):
        self.label_basic_sketch_synid = customtkinter.CTkLabel(self.frame, text="Basic Sketch Synopsis ID")
        self.label_basic_sketch_synid .grid(row=1, column=0, padx=20, pady=(10, 10))
        self.basic_sketch_syn_id = customtkinter.CTkEntry(master=self.frame, placeholder_text="1")
        self.basic_sketch_syn_id.grid(row=1, column=1, padx=20, pady=(10, 10))


        self.bt_choose_basic_sketch = customtkinter.CTkButton(self.frame, text="Step 2: Choose Basic Sketch",
                                                        height=50, command=self.spatial_sketch_parameters)
        self.bt_choose_basic_sketch.grid(row=2, column=0, padx=20, pady=(10, 10))

    def spatial_sketch_parameters(self):
        syn = self.synMap["30"]
        self.basicSketchSynId = self.basic_sketch_syn_id.get()
        self.basic_sketch_syn_id.destroy()
        self.label_basic_sketch_synid.destroy()
        self.bt_choose_basic_sketch.destroy()
        if (self.basicSketchSynId not in self.synMap):
            messagebox.showerror("Error", "Invalid Basic Sketch Synopsis ID", parent=self.frame)
            return
        basicSyn = self.synMap[self.basicSketchSynId]

        self.parameters = customtkinter.CTkFrame(self.frame, width=250, height=250, fg_color="#000811")
        self.parameters.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        label_synopsis = customtkinter.CTkLabel(self.parameters, text="Parameters for {}".format(syn["name"]),
                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        label_synopsis.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
        i = 0
        parameters = []
        for param in syn["parameters"]:
            if param == "BasicSketchParameters" or param == "BasicSketchSynID":
                continue
            label = customtkinter.CTkLabel(self.parameters, text=param, font=customtkinter.CTkFont(size=14))
            label.grid(row=i+1, column=0, padx=20, pady=(10, 10))
            entry = customtkinter.CTkEntry(master=self.parameters, placeholder_text=param)
            entry.grid(row=i+1, column=1, padx=20, pady=(10, 10))
            parameters.append(entry)
            i += 1

        self.parametersBasic = customtkinter.CTkFrame(self.frame, width=250, height=250, fg_color="#000811")
        self.parametersBasic.grid(row=1, column=5, padx=(20, 20), pady=(20, 0), sticky="nsew")
        label_synopsis = customtkinter.CTkLabel(self.parametersBasic, text="Parameters for basic sketch {}".format(basicSyn["name"]),
                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        label_synopsis.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
        for i, param in enumerate(basicSyn["parameters"]):
            label = customtkinter.CTkLabel(self.parametersBasic, text=param, font=customtkinter.CTkFont(size=14))
            label.grid(row=i + 1, column=0, padx=20, pady=(10, 10))
            entry = customtkinter.CTkEntry(master=self.parametersBasic, placeholder_text=param)
            entry.grid(row=i + 1, column=1, padx=20, pady=(10, 10))

        self.parametersBasic.get = lambda: ";".join([e.get() for e in self.parametersBasic.winfo_children() if isinstance(e, customtkinter.CTkEntry)])
        # overwrite self.parameters.get() to return a string of parameters seperated by ", "
        self.parameters.get = lambda: ", ".join([e.get() for e in self.parameters.winfo_children() if isinstance(e, customtkinter.CTkEntry)])

        bt_create_synopsis = customtkinter.CTkButton(self.frame, text="Step 3: Choose synopsis specific parameters",
                                                     height=50, command=self.send_request)
        bt_create_synopsis.grid(row=2, column=0, padx=20, pady=(10, 10))

    def custom_parameters(self, syn):
        self.parameters = customtkinter.CTkFrame(self.frame, width=250, height=250, fg_color="#000811")
        self.parameters.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        label_synopsis = customtkinter.CTkLabel(self.parameters, text="Parameters for {}".format(syn["name"]),
                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        label_synopsis.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
        for i, param in enumerate(syn["parameters"]):
            label = customtkinter.CTkLabel(self.parameters, text=param, font=customtkinter.CTkFont(size=14))
            label.grid(row=i+1, column=0, padx=20, pady=(10, 10))
            entry = customtkinter.CTkEntry(master=self.parameters, placeholder_text=param)
            entry.grid(row=i+1, column=1, padx=20, pady=(10, 10))

        # overwrite self.parameters.get() to return a string of parameters seperated by ", "
        self.parameters.get = lambda: ", ".join([e.get() for e in self.parameters.winfo_children() if isinstance(e, customtkinter.CTkEntry)])

    def send_request(self):
        # 1 because requestId 1 is creating a synopsis.
        if self.parameters.get() == "":
            messagebox.showerror("Error", "Please fill in all fields", parent=self.frame)
            return
        synParameters = self.parameters.get().split(", ")
        synBasicParameters = self.parametersBasic.get()
        synParameters = self.get_correct_parameters(synParameters, synBasicParameters)
        print(synParameters)
        print(synBasicParameters)
        rq = SendRequest(1, self.datasetKey.get(), self.streamID.get(), self.UID.get(),
                         self.SynopsisID.get(), self.NoOfP.get(), synParameters, self.App)

        #rq = SendRequest(par, synParameters)

        rq.send_request_to_kafka_topic()
        messagebox.showinfo("Request Sent", "Request sent to Kafka Topic", parent=self.frame)

    # def setFrame2(self, frame, main_container):
    #     self.frame = frame
    #     self.main_container = main_container
    #     self.App.title("change title here")
    #     # create synopsis frame
    #     frame = customtkinter.CTkFrame(self.main_container)
    #     # set title
    #     title = customtkinter.CTkLabel(frame, text="Create Synopsis",
    #                                    font=customtkinter.CTkFont(size=20, weight="bold"))
    #     title.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)
    #
    #     # make Request class with textboxes for datasetkey, streamID, UID, SynopsisID, NoOfP and parameters
    #
    #     dataEntry = customtkinter.CTkFrame(frame, width=250, height=250, fg_color="#000811")
    #
    #     dataEntry.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
    #     label_dataEntry = customtkinter.CTkLabel(dataEntry, text="Synopsis Parameters",
    #                                              font=customtkinter.CTkFont(size=15, weight="bold"))
    #     label_dataEntry.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
    #     self.datasetKey = customtkinter.CTkEntry(master=dataEntry, placeholder_text="DatasetKey")
    #     self.datasetKey.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="n")
    #     self.streamID = customtkinter.CTkEntry(master=dataEntry, placeholder_text="StreamID")
    #     self.streamID.grid(row=2, column=0, padx=20, pady=(10, 10))
    #     self.UID = customtkinter.CTkEntry(master=dataEntry, placeholder_text="UID")
    #     self.UID.grid(row=3, column=0, padx=20, pady=(10, 10))
    #     self.SynopsisID = customtkinter.CTkEntry(master=dataEntry, placeholder_text="SynopsisID")
    #     self.SynopsisID.grid(row=4, column=0, padx=20, pady=(10, 10))
    #     self.NoOfP = customtkinter.CTkEntry(master=dataEntry, placeholder_text="NoOfP")
    #     self.NoOfP.grid(row=5, column=0, padx=20, pady=(10, 10))
    #     self.parameters = customtkinter.CTkEntry(master=dataEntry, width=250, placeholder_text="Parameters")
    #     self.parameters.grid(row=6, column=0, padx=20, pady=(10, 10))
    #     dataEntry.place(relx=0.2, rely=0.5, anchor=customtkinter.CENTER)
    #
    #     # create a button to send the request to the kafka topic
    #     bt_create_synopsis = customtkinter.CTkButton(frame, text="Create Synopsis", height=50,
    #                                                  command=self.send_request)
    #     bt_create_synopsis.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
    #     #
    #     # # create a button to send the request to the kafka topic
    #     # bt_from_frame2 = customtkinter.CTkButton(frame, text="Test 2", command=lambda: print("test 2"))
    #     # bt_from_frame2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    #     return frame, main_container
    def get_correct_parameters(self, synParameters, synBasicParameters):
        if self.SynopsisID.get() == "30":
            new_parameters = [synParameters[0], synParameters[1], synParameters[2], synBasicParameters,
                              self.basicSketchSynId, synParameters[3], synParameters[4], synParameters[5],
                              synParameters[6], synParameters[7]]
            synParameters = new_parameters
        return synParameters
        pass



