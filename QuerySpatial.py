
import tkinter as tk
import customtkinter
import json
import os
from PIL import Image, ImageTk, ImageOps

from CustomCTkTable import *
import threading
from tkinter import messagebox, ttk

# from confluent_kafka import *
from ScrollableRadioButtonFrame import ScrollableRadiobuttonFrame
from datasetMap import DatasetMap


class QuerySpatial:
    frame = None

    def __init__(self, App):
        # App
        self.App = App

        # Current synopsis

        # Windows
        self.img_window_ctk = None # Window for the image
        self.grid_window_ctk = None # Window for the grid

        # Widgets
        self.button_load_synopses = None
        self.scrollable_frame_synopses = None
        self.table = None

        # Dataset map
        self.dsMap = None

        self.scrollable_frame = None
        self.output = None
        self.frame = None
        self.labels = ["Estimate:"]
        self.entry_widgets = {}


        self.selected_cells = []

        # Current synopsis
        self.curU_name = None
        self.curUID = None
        self.curStreamID = None
        self.curDatasetKey = None
        self.curSynopsisID = None
        self.curNoOfP = None
        self.curParameters = None

        self.minY = None
        self.maxY = None
        self.minX = None
        self.maxX = None
        self.resolution = None

        self.curMaxCol = None
        self.curMinCol = None
        self.curMaxRow = None
        self.curMinRow = None

    def set_query_parameters(self):
        self.setCurSynopsis(self.scrollable_frame.get_checked_item())

        # request class with textboxes for datasetkey, streamID, UID, SynopsisID, NoOfP and parameters
        self.dataEntry = customtkinter.CTkFrame(self.frame, width=200, height=250, fg_color="#000811")

        self.dataEntry.grid(row=2, columnspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        label_dataEntry = customtkinter.CTkLabel(self.dataEntry, text="Step 2: Choose Query Parameters",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        label_dataEntry.grid(row=0, columnspan=4, padx=20, pady=(10, 10), sticky="nsew")

        if self.dsMap is None:
            label = customtkinter.CTkLabel(self.dataEntry, text="Custom Parameters",
                                           font=customtkinter.CTkFont(size=14))
            label.grid(row=1, column=0, padx=20, pady=(10, 10))
            entry = customtkinter.CTkEntry(master=self.dataEntry, width=250, placeholder_text="Query Parameters")
            entry.grid(row=1, column=1, padx=20, pady=(10, 10))
        else:
            for i, label_text in enumerate(self.dsMap["queryParameters"]):
                label = customtkinter.CTkLabel(self.dataEntry, text=label_text,
                                               font=customtkinter.CTkFont(size=14))
                label.grid(row=i + 1, column=0, padx=20, pady=(10, 10))
                entry = customtkinter.CTkEntry(master=self.dataEntry, width=250, placeholder_text=label_text)
                entry.grid(row=i + 1, column=1, padx=20, pady=(10, 10))
        self.dataEntry.get = lambda: ", ".join([e.get() for e in self.dataEntry.winfo_children() if isinstance(e, customtkinter.CTkEntry)])
        #     queryParameters = customtkinter.CTkEntry(master=self.dataEntry, width=250,
        #                                               placeholder_text="Query Parameters")
        # self.queryParameters.grid(row=1, column=0, padx=20, pady=(10, 10))

        # Button to show the grid
        self.create_grid()

        # create a button to send the request to the kafka topic
        bt_query_synopsis = customtkinter.CTkButton(master=self.frame, text="Submit Query",
                                                    command=self.send_request)
        bt_query_synopsis.grid(row=3,columnspan=2, padx=(20, 0), pady=(20, 20))

    def create_grid(self):
        # First destroy the existing grid
        if self.img_window_ctk is not None:
            self.img_window_ctk.destroy()
        if self.grid_window_ctk is not None:
            self.grid_window_ctk.destroy()

        # Check if syn_array has at least 5 elements

        self.curMaxCol = 0#int(self.minX)
        self.curMinCol = self.resolution#int(self.maxX)
        self.curMaxRow = 0#int(self.minY)
        self.curMinRow = self.resolution#int(self.maxY)

        sizeY = int(self.maxY) - int(self.minY)
        sizeX = int(self.maxX) - int(self.minX)

        # we always want a 1000x1000 grid
        self.desiredSize = min(self.App.winfo_screenwidth(), self.App.winfo_screenheight())
        scaleFactorX = self.desiredSize / sizeX
        scaleFactorY = self.desiredSize / sizeY
        self.img_window_ctk = customtkinter.CTkToplevel(self.App)
        self.img_window = customtkinter.CTkFrame(self.img_window_ctk)

        self.img_window_ctk.geometry("{}x{}".format(self.desiredSize, self.desiredSize))

        #self.img_window_ctk.geometry = self.App.geometry#("{0}x{0}+0+0".format(self.App.winfo_screenwidth(), self.App.winfo_screenheight()))
        self.img_window_ctk.title("Step 3: Choose parameters")

        self.img_window_ctk.resizable(False, False)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        img = Image.open(os.path.join(image_path, "europe_arcgis.png"))
        img = ImageOps.fit(img, (self.desiredSize, self.desiredSize))
        img_width, img_height = img.size
        self.europe_map_image = customtkinter.CTkImage(img, size=(img_width, img_height))
        label_image = customtkinter.CTkLabel(self.img_window, text="", image=self.europe_map_image)
        label_image.image = self.europe_map_image
        label_image.place(relx=0.5, rely=0.5, anchor="center")
        label_image.pack()
        self.img_window.pack(fill=tkinter.BOTH, expand=True, padx=0, pady=0)

        self.grid_window_ctk = customtkinter.CTkToplevel(self.App)
        # self.grid_window_ctk.geometry("{}x{}".format(self.desiredSize, self.desiredSize))
        self.grid_window_ctk.geometry("{}x{}".format(img_width, img_height))

        #self.grid_window_ctk.geometry = self.App.geometry#("{0}x{0}+0+0".format(self.App.winfo_screenwidth(), self.App.winfo_screenheight()))
        self.grid_window_ctk.resizable(False, False)

        #grid_window_ctk.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        self.grid_window_ctk.title("Step 3: Choose parameters")
        self.grid_window_ctk.wait_visibility(self.grid_window_ctk)
        self.grid_window_ctk.wm_attributes("-alpha", 0.4)
        grid_window = customtkinter.CTkFrame(self.grid_window_ctk)

        self.table = CTkTable(master=grid_window, row=self.resolution,
                              column=self.resolution, width=self.desiredSize, height=self.desiredSize,
                              padx=0,
                              hover_color="#f0f0f0")
        self.table.grid(row=0, column=0, padx=0, pady=0)
        self.grid_window_ctk.bind("<Configure>", self.move_me)
        self.img_window_ctk.attributes("-topmost", True)
        self.grid_window_ctk.attributes("-topmost", True)

        grid_window.pack(fill=tkinter.BOTH, expand=True, padx=0, pady=0)


    def move_me(self, event):
        try:
            if self.img_window_ctk is not None:
                x = self.grid_window_ctk.winfo_x()
                y = self.grid_window_ctk.winfo_y()
                offset = 37

                # Set the position of img_window_ctk
                self.img_window_ctk.geometry(f"+{x}+{y - offset}")
                #self.img_window_ctk.geometry(f"{self.desiredSize}x{self.desiredSize}+{x}+{y}")

        except NameError:
            pass

    def store_cell(self, e):
        row = e['row']
        col = e['column']
        val = e['value']
        if row < self.curMinRow:
            self.curMinRow = row
        if row > self.curMaxRow:
            self.curMaxRow = row
        if col < self.curMinCol:
            self.curMinCol = col
        if col > self.curMaxCol:
            self.curMaxCol = col
        self.selected_cells.append({"row": row, "col": col, "val": val})

    def set_frame4(self):
        self.frame = self.App.frames["frame4"]
        # if (self.App.current_dataset != None):
        #     self.dsMap = DatasetMap.getDataset(DatasetMap(), self.App.current_dataset["DatasetName"])

        # set title
        title = customtkinter.CTkLabel(self.frame, text="Query Synopsis",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        title.place(relx=0.5, rely=0.02, anchor=customtkinter.CENTER)
        self.create_existing_synopsis_frame()
        self.create_widgets()

        self.App.frames["frame4"] = self.frame

    def getSelectedCells(self):
        #reset old pars
        self.curMaxCol = 0#int(self.minX)
        self.curMinCol = self.resolution#int(self.maxX)
        self.curMaxRow = 0#int(self.minY)
        self.curMinRow = self.resolution#int(self.maxY)

        # go over all cells in table and store the selected ones
        self.selected_cells = []
        for i in range(self.resolution):
            for j in range(self.resolution):
                if isinstance(self.table.frame[i, j], CustomCTkCheckBox):
                    if self.table.frame[i, j].get() == 1:
                        print("Cell: ", i, j, " is selected")
                        self.store_cell({"row": i, "column": j, "value": 1})

    def send_request(self):
        self.getSelectedCells()
        basicSketchQueryParameters = self.dataEntry.get().replace(" ", "").split(",") + "1".split(",")
        if len(basicSketchQueryParameters) != 2:
            messagebox.showerror("Error",
                                 "Please enter the two parameters for CountMin in SpatialSketch", parent=self.frame)
            return
        # check if the user has selected a grid
        if len(self.selected_cells) == 0:
            messagebox.showerror("Error", "Please select a grid", parent=self.frame)
            return

        # get dtypes of the parameters
        self.minX = int(self.minX)
        self.maxX = int(self.maxX)
        self.minY = int(self.minY)
        self.maxY = int(self.maxY)
        #scale curMinRow, curMaxRow, curMinCol, curMaxCol to be absolute values based on grid
        curMinValX = int(self.minX + (self.curMinCol * (self.maxX - self.minX) / self.resolution))
        curMaxValX = int(self.minX + (self.curMaxCol * (self.maxX - self.minX) / self.resolution))
        curMinValY = int(self.minY + (self.curMinRow * (self.maxY - self.minY) / self.resolution))
        curMaxValY = int(self.minY + (self.curMaxRow * (self.maxY - self.minY) / self.resolution))
        queryParameters = [basicSketchQueryParameters[0], basicSketchQueryParameters[1], str(curMinValX),
                           str(curMaxValX),
                           str(curMinValY), str(curMaxValY)]

        # rq = SendRequest(3, self.curDatasetKey, self.curStreamID, self.curU_name, self.curUID, self.curSynopsisID,
        #                  self.curNoOfP, queryParameters, self.App)
        # rq.send_request_to_kafka_topic()

        rq = {"key":self.curDatasetKey, "streamID":self.curStreamID, "synopsisID":self.curSynopsisID, "requestID":3,
              "dataSetkey": self.curDatasetKey, "param": queryParameters,"noOfP":self.curNoOfP, "uid":self.curUID,
              "externalUID":"Estimate:"+str(self.curUID)}
        self.App.sde.send_request(rq, "Estimate:"+str(self.curUID))

        # small timeout
        messagebox.showinfo("Query Successful", "Query successfully submitted.", parent=self.frame)

    def create_widgets(self):

        # self.output = customtkinter.CTkFrame(self.frame, width=250, height=250, fg_color="#000811")

        self.output = customtkinter.CTkFrame(self.frame, width=500, height=250, fg_color="#000811")
        # self.output.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        label_output = customtkinter.CTkLabel(self.output, text="Query Output",
                                              font=customtkinter.CTkFont(size=15, weight="bold"))
        label_output.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.output.place(relx=0.75, rely=0.25, anchor=customtkinter.CENTER)

        # grid for
        for i, label_text in enumerate(self.labels):
            label = customtkinter.CTkLabel(self.output, text=label_text, font=customtkinter.CTkFont(size=14))
            label.grid(row=i + 1, column=0, padx=20, pady=(10, 10))

            self.entry_widgets[label_text] = customtkinter.CTkTextbox(self.output, width=500, height=250,
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
                    if m['synopsisID'] != 30:
                        continue
                    estimate = m["estimation"]
                    param = m["param"]

                    self.entry_widgets["Estimate:"].insert(customtkinter.END,
                                                               "\n" + "Query " + str(queryCounter) +
                                                               " with parameters: " +
                                                               str(param) +
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
            if self.App.existing_synopses[syn]["synopsisID"] == '30':
                self.scrollable_frame.add_item(self.App.existing_synopses[syn])

    def load_existing_synopses(self):
        self.button_load_synopses.destroy()
        self.button_load_synopses = customtkinter.CTkButton(self.frame,
                                                            text="Reload Synopses",
                                                            command=self.reload_existing_synopses)
        self.button_load_synopses.grid(row=0, column=0, padx=(20, 0), pady=(50, 0))


        self.scrollable_frame = ScrollableRadiobuttonFrame(master=self.frame,
                                                           item_list=self.App.existing_synopses,
                                                           command=self.set_query_parameters,
                                                           label_text="Step 1: Load Existing Synopses", width=650,
                                                           height=400, fg_color="#000811")
        self.scrollable_frame.grid(row=1, columnspan=4, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.reload_existing_synopses()

    def setCurSynopsis(self, syn):
        self.curDatasetKey = syn['dataSetkey']
        self.curStreamID = syn['streamID']

        self.curU_name = syn['u_name']
        self.curUID = syn['uid']
        self.curSynopsisID = syn['synopsisID']
        self.curNoOfP = syn['noOfP']
        self.curParameters = syn['param']

        print("Current selected synopsis: ", syn)
        # only for spatial synopses
        self.minX = syn['param'][-5]
        self.maxX = syn['param'][-4]
        self.minY = syn['param'][-3]
        self.maxY = syn['param'][-2]
        self.resolution = int(syn['param'][-1])

