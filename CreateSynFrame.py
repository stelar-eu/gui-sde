
from tkinter import messagebox

import customtkinter
from messages.sendRequest import SendRequest
from synMap import SynMap


class CreateSynFrame:
    main_container = None
    frame = None

    datasetKey = None
    streamID = None
    u_name = None
    synopsis_type_dropdown = None
    NoOfP = None
    parameters = None

    def __init__(self, App):
        # Application
        self.App = App

        # Maps with synopses
        self.synMap = SynMap.getSynMap(SynMap())
        self.basicSketchMap = SynMap.getBasicSketches(SynMap())

        # Frames
        self.dataEntry = None
        self.basic_sketch_dropdown = None

        # Buttons
        self.bt_create_synopsis = None
        self.bt_choose_basic_sketch = None
        self.bt_send_synopsis_request = None

        # Basic sketch name
        self.label_basic_sketch_synid = None
        self.basic_sketch_name = None

        # Basic sketch parameters
        self.parametersBasic = None

        # copy synopsis frame
        self.frame = self.App.frames["frame2"]

    def set_synopsis_id(self, event):
        return str(self.synMap[event]["synID"])

    def load_synopsis_parameters_frame(self):
        self.dataEntry = customtkinter.CTkFrame(self.frame, width=250, height=250, fg_color="#000811")
        self.data_entry_row = 0

        self.dataEntry.grid(row=self.data_entry_row, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.label_dataEntry = customtkinter.CTkLabel(self.dataEntry, text="Select Dataset and Synopsis Type",
                                                      font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_dataEntry.grid(row=self.data_entry_row, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.data_entry_row += 1

        if self.App.current_dataset is None:
            label_datasetKey = customtkinter.CTkLabel(self.dataEntry, text="DatasetKey")
            label_datasetKey.grid(row=self.data_entry_row, column=0, padx=20, pady=(10, 10), sticky="n")
            self.datasetKey = customtkinter.CTkEntry(master=self.dataEntry, placeholder_text="DatasetKey")
            self.datasetKey.grid(row=self.data_entry_row, column=1, padx=20, pady=(10, 10), sticky="n")
            self.data_entry_row += 1

            label_streamID = customtkinter.CTkLabel(self.dataEntry, text="StreamID")
            label_streamID.grid(row=self.data_entry_row, column=0, padx=20, pady=(10, 10))
            self.streamID = customtkinter.CTkEntry(master=self.dataEntry, placeholder_text="StreamID")
            self.streamID.grid(row=self.data_entry_row, column=1, padx=20, pady=(10, 10))
            self.data_entry_row += 1
        else:
            self.datasetKey = self.App.current_dataset['DatasetKey']
            self.streamID = self.App.current_dataset['StreamID']

        label_UID = customtkinter.CTkLabel(self.dataEntry, text="Unique Name")
        label_UID.grid(row=self.data_entry_row, column=0, padx=20, pady=(10, 10))
        self.u_name = customtkinter.CTkEntry(master=self.dataEntry, placeholder_text="Unique Name")
        self.u_name.grid(row=self.data_entry_row, column=1, padx=20, pady=(10, 10))
        self.data_entry_row += 1

        label_SynopsisID = customtkinter.CTkLabel(self.dataEntry, text="Query Type - Synopsis Name")
        label_SynopsisID.grid(row=self.data_entry_row, column=0, padx=20, pady=(10, 10))

        # default is countmin:
        default_var = customtkinter.StringVar(value=list(self.synMap.keys())[0])
        self.synopsis_type_dropdown = customtkinter.CTkComboBox(master=self.dataEntry, values=list(self.synMap.keys()),
                                                                command=self.set_synopsis_id, variable=default_var)
        #self.SynopsisID = customtkinter.CTkEntry(master=self.dataEntry, placeholder_text="SynopsisID")
        self.synopsis_type_dropdown.grid(row=self.data_entry_row, column=1, padx=20, pady=(10, 10))
        self.data_entry_row += 1

        # label_NoOfP = customtkinter.CTkLabel(self.dataEntry, text="Number of partitions")
        # label_NoOfP.grid(row=self.data_entry_row, column=0, padx=20, pady=(10, 10))
        # self.NoOfP = customtkinter.CTkEntry(master=self.dataEntry, placeholder_text="16")
        # self.NoOfP.grid(row=self.data_entry_row, column=1, padx=20, pady=(10, 10))
        self.data_entry_row += 1

        self.dataEntry.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # create a button to send the request to the kafka topic
        self.bt_create_synopsis = customtkinter.CTkButton(self.dataEntry, text="Select", height=50,
                                                          command=self.choose_parameters)
        self.bt_create_synopsis.grid(row=self.data_entry_row, column=0, padx=20, pady=(10, 10))
        self.data_entry_row += 1

    def set_frame2(self):
        # set title
        title = customtkinter.CTkLabel(self.frame, text="Create Synopsis",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        title.place(relx=0.5, rely=0.02, anchor=customtkinter.CENTER)

        # make Request class with textboxes for datasetkey, streamID, UID, SynopsisID, NoOfP and parameters
        self.load_synopsis_parameters_frame()

        self.App.frames["frame2"] = self.frame

    def choose_parameters(self):
        if self.basic_sketch_dropdown is not None:
            self.basic_sketch_dropdown.destroy()
        if self.label_basic_sketch_synid is not None:
            self.basic_sketch_name = None
            self.label_basic_sketch_synid.destroy()
        if self.bt_choose_basic_sketch is not None:
            self.bt_choose_basic_sketch.destroy()
        if self.parameters is not None:
            self.parameters.destroy()
        if self.parametersBasic is not None:
            self.parametersBasic.destroy()
        if self.bt_send_synopsis_request is not None:
            self.bt_send_synopsis_request.destroy()
        self.bt_create_synopsis.configure(text="Reselect")
        #
        # synID = self.SynopsisID.get()

        if self.synopsis_type_dropdown.get() == "" or self.u_name.get() == "":
            if isinstance(self.datasetKey, str) or isinstance(self.streamID, str):
                if self.datasetKey == "" or self.streamID == "" or self.u_name.get() == "":
                    messagebox.showerror("Error", "Please fill in all fields", parent=self.frame)
            elif self.datasetKey.get() == "" or self.streamID.get() == "":
                messagebox.showerror("Error", "Please fill in all fields", parent=self.frame)
            return
        # if synID not in self.synMap:
        #     messagebox.showerror("Error", "Invalid Synopsis ID", parent=self.frame)
        #     return
        if self.u_name.get() in self.App.existing_synopses:
            messagebox.showerror("Error", "Unique Name {} already exists".format(self.u_name.get()), parent=self.frame)
            return

        if self.synopsis_type_dropdown.get() == "Spatial Queries - SpatialSketch":
            # in spatial sketch, have to choose basic sketch
            self.choose_basic_sketch()
        else:
            if self.synopsis_type_dropdown.get() in self.synMap:
                self.custom_parameters(self.synMap[self.synopsis_type_dropdown.get()])
            else:
                self.parameters = customtkinter.CTkEntry(master=self.frame, width=250, placeholder_text="Parameters")
                self.parameters.grid(row=1, column=0, padx=20, pady=(10, 10))

            self.bt_send_synopsis_request = customtkinter.CTkButton(self.frame, text="Create Synopsis",
                                                         height=50, command=self.send_request)
            self.bt_send_synopsis_request.grid(row=2, column=0, padx=20, pady=(10, 10))

    def choose_basic_sketch(self):
        self.label_basic_sketch_synid = customtkinter.CTkLabel(self.dataEntry, text="Basic Sketch Synopsis ID")
        self.label_basic_sketch_synid .grid(row=self.data_entry_row, column=0, padx=20, pady=(10, 10))
        self.basic_sketch_dropdown = customtkinter.CTkComboBox(master=self.dataEntry, values=list(self.basicSketchMap.keys()))

        #self.basic_sketch_syn_id = customtkinter.CTkEntry(master=self.dataEntry, placeholder_text="1")
        self.basic_sketch_dropdown.grid(row=self.data_entry_row, column=1, padx=20, pady=(10, 10))
        self.data_entry_row += 1

        self.bt_choose_basic_sketch = customtkinter.CTkButton(self.dataEntry, text="Select Basic Sketch",
                                                        height=50, command=self.spatial_sketch_parameters)
        self.bt_choose_basic_sketch.grid(row=self.data_entry_row, column=0, padx=20, pady=(10, 10))
        self.data_entry_row += 1

    def spatial_sketch_parameters(self):
        self.bt_choose_basic_sketch.configure(text="Reselect Basic Sketch")

        syn = self.synMap["Spatial Queries - SpatialSketch"]
        self.basic_sketch_name = self.basic_sketch_dropdown.get()
        # self.basic_sketch_syn_id.destroy()
        # self.label_basic_sketch_synid.destroy()
        # self.bt_choose_basic_sketch.destroy()
        if self.basic_sketch_name not in self.synMap:
            messagebox.showerror("Error", "Invalid Basic Sketch", parent=self.frame)
            return
        basicSyn = self.synMap[self.basic_sketch_name]

        self.parameters = customtkinter.CTkFrame(self.frame, width=250, height=250, fg_color="#000811")
        self.parameters.grid(row=2, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        label_synopsis = customtkinter.CTkLabel(self.parameters, text="Parameters for {}".format(syn["name"]),
                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        label_synopsis.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
        i = 0
        parameters = []
        for param in syn["parameters"]:
            default_param = ""
            if param == "keyField" or param == "valueField" or param == "operationMode":
                # Will be selected by basic sketch
                continue
            if param == "BasicSketchParameters" or param == "BasicSketchSynID":
                # Selected in previous step
                continue
            if self.App.current_dataset is not None and param in ["minX", "maxX", "minY", "maxY"]:
                # Already known
                continue
            label = customtkinter.CTkLabel(self.parameters, text=param, font=customtkinter.CTkFont(size=14))
            label.grid(row=i+1, column=0, padx=20, pady=(10, 10))

            if param == "maxResolution":
                default_param = "16"

            stringVar = customtkinter.StringVar(value=default_param)
            entry = customtkinter.CTkEntry(master=self.parameters, placeholder_text=param, textvariable=stringVar)
            entry.grid(row=i+1, column=1, padx=20, pady=(10, 10))
            parameters.append(entry)
            i += 1

        self.parametersBasic = customtkinter.CTkFrame(self.frame, width=250, height=250, fg_color="#000811")
        self.parametersBasic.grid(row=2, column=5, padx=(20, 20), pady=(20, 0), sticky="nsew")
        label_synopsis = customtkinter.CTkLabel(self.parametersBasic, text="Parameters for basic sketch {}".format(basicSyn["name"]),
                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        label_synopsis.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
        for i, param in enumerate(basicSyn["parameters"]):
            default_param = ""
            label = customtkinter.CTkLabel(self.parametersBasic, text=param, font=customtkinter.CTkFont(size=14))
            label.grid(row=i + 1, column=0, padx=20, pady=(10, 10))
            if (param == "keyField" or param == "valueField") and self.App.current_dataset is not None:
                print("current dataset", self.App.current_dataset["parameters"])
                dropdown = customtkinter.CTkComboBox(master=self.parametersBasic, values=self.App.current_dataset["parameters"])
                dropdown.grid(row=i + 1, column=1, padx=20, pady=(10, 10))
            else:
                if param == "operationMode":
                    default_param = "Queryable"
                elif param == "epsilon":
                    default_param = "0.002"
                elif param == "confidence":
                    default_param = "0.99"
                elif param == "seed":
                    default_param = "1"
                stringVar = customtkinter.StringVar(value=default_param)
                entry = customtkinter.CTkEntry(master=self.parametersBasic, placeholder_text=default_param, textvariable=stringVar)
                entry.grid(row=i + 1, column=1, padx=20, pady=(10, 10))

        self.parametersBasic.get = lambda: ";".join([e.get() for e in self.parametersBasic.winfo_children()
                                                     if (isinstance(e, customtkinter.CTkEntry)
                                                         or isinstance(e, customtkinter.CTkComboBox))])
        # overwrite self.parameters.get() to return a string of parameters seperated by ", "
        self.parameters.get = lambda: ", ".join([e.get() for e in self.parameters.winfo_children() if isinstance(e, customtkinter.CTkEntry)])

        self.bt_send_synopsis_request = customtkinter.CTkButton(self.frame, text="Create Synopsis",
                                                                height=50, command=self.send_request)
        self.bt_send_synopsis_request.grid(row=3, column=0, padx=20, pady=(10, 10))

    def custom_parameters(self, syn):
        self.parameters = customtkinter.CTkFrame(self.frame, width=250, height=250, fg_color="#000811")
        self.parameters.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        label_synopsis = customtkinter.CTkLabel(self.parameters, text="Parameters for {}".format(syn["name"]),
                                                font=customtkinter.CTkFont(size=15, weight="bold"))
        label_synopsis.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
        for i, param in enumerate(syn["parameters"]):
            label = customtkinter.CTkLabel(self.parameters, text=param, font=customtkinter.CTkFont(size=14))
            label.grid(row=i + 1, column=0, padx=20, pady=(10, 10))
            if (param == "keyField" or param == "valueField") and self.App.current_dataset is not None:
                dropdown = customtkinter.CTkComboBox(master=self.parameters, values=self.App.current_dataset["parameters"],
                                                     variable=customtkinter.StringVar(value=self.App.current_dataset["parameters"][0]))
                dropdown.grid(row=i + 1, column=1, padx=20, pady=(10, 10))
            else:
                entry = customtkinter.CTkEntry(master=self.parameters, placeholder_text=param)
                entry.grid(row=i+1, column=1, padx=20, pady=(10, 10))

        # overwrite self.parameters.get() to return a string of parameters seperated by ", "
        self.parameters.get = lambda: ", ".join([e.get() for e in self.parameters.winfo_children() if (isinstance(e, customtkinter.CTkEntry)
                                                                                                       or isinstance(e, customtkinter.CTkComboBox))])

    def send_request(self):
        # 1 because requestId 1 is creating a synopsis.
        if self.parameters.get() == "":
            messagebox.showerror("Error", "Please fill in all fields", parent=self.frame)
            return
        synParameters = self.parameters.get().split(", ")
        if self.synopsis_type_dropdown.get() == "Spatial Queries - SpatialSketch":
            synBasicParameters = self.parametersBasic.get()
            synParameters = self.get_correct_parameters(synParameters, synBasicParameters)

        if isinstance(self.datasetKey, str):
            req_datasetKey = self.datasetKey
        else:
            req_datasetKey = self.datasetKey.get()

        if isinstance(self.streamID, str):
            req_streamID = self.streamID
        else:
            req_streamID = self.streamID.get()

        print("parallelization", self.App.parallelization.get())

        rq = SendRequest(1, req_datasetKey, req_streamID, self.u_name.get(), None,
                         self.set_synopsis_id(self.synopsis_type_dropdown.get()),
                         self.App.parallelization.get(), synParameters, self.App)

        rq.send_request_to_kafka_topic()
        messagebox.showinfo("Synopsis Created", "Synopsis successfully created.", parent=self.frame)

    def get_correct_parameters(self, synParameters, synBasicParameters):
        basic_parameters = synBasicParameters.split(";")
        if self.App.current_dataset is not None: # use current dataset in frame 1
            minX = str(self.App.current_dataset["minX"])
            maxX = str(self.App.current_dataset["maxX"])
            minY = str(self.App.current_dataset["minY"])
            maxY = str(self.App.current_dataset["maxY"])
            res = synParameters[0]
        else:
            minX = synParameters[0]
            maxX = synParameters[1]
            minY = synParameters[2]
            maxY = synParameters[3]
            res = synParameters[4]

        new_parameters = [basic_parameters[0], basic_parameters[1], basic_parameters[2], synBasicParameters,
                          str(self.basicSketchMap[self.basic_sketch_name]["synID"]), minX, maxX, minY, maxY, res]
        return new_parameters


