import ast
import os
import re
import threading
import tkinter
import tkinter.messagebox
from tkinter import messagebox

import json
import customtkinter

import subprocess
from customtkinter import CTk

from CreateSynFrame import CreateSynFrame
from QueryNormal import QueryNormal
from QuerySpatial import QuerySpatial
from DataManagement import DataManagement
from datasetMap import DatasetMap
#
from sde_py_lib.client import Client
from stelar.client import Client as stelarClient
from sde_py_lib.model import Synopsis, SynopsisSpec

from PIL import Image, ImageTk, ImageOps

from messages.Request import Request


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

num_frames = 4
#"data_topic" "request_topic" "OUT" "localhost:9092" "2"


def add_to_file(data, filename):
    if os.path.isfile(filename):
        with open(filename, "a") as file:
            file.write(str(data) + "\n")
    else:
        with open(filename, "w") as file:
            file.write(str(data) + "\n")

def load_credentials(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def extract_json_from_content(data):
    if data:
        content = data['content']
        #
        # content = data['content']
        # # Extract JSON-like structure from 'content'
        # # match = re.search(r'Existing Synopsis: ({.*})', content, re.DOTALL)
        # match = re.search(r'Syn_({.*})', content, re.DOTALL)
        #
        # if match:
        #     json_str = match.group(1).replace('\n', '').replace(' ', '')
        #     try:
        #         return json.loads(json_str)
        #     except json.JSONDecodeError:
        #         print("Invalid JSON structure in 'content'.")
        # return None

        matches = re.findall(r'Syn_\d+_\{(.*?)\}', content, re.DOTALL)
        synopses = []

        for match in matches:
            json_str = '{' + match.strip().replace('\n', '').replace(' ', '') + '}'
            try:
                synopses.append(json.loads(json_str))
            except json.JSONDecodeError:
                print("Invalid JSON structure in 'content'.")

        return synopses


def read_metainfo_existing_datasets():
    # Here, we read the datasets.txt file.
    # The file should contain a list of dictionaries, each representing a dataset.
    # Each dictionary should contain the following keys:
    # - dataSetkey
    # - DatasetName
    # - StreamID
    # - Attribute list

    with open("datasets.txt", "r") as file:
        datasets = file.readlines()
        existing_datasets = {}
        for d in datasets:
            dataset = ast.literal_eval(d)

            existing_datasets[dataset["dataSetkey"]] = dataset
        return existing_datasets



class App(customtkinter.CTk):
    frames = {"frame1": None, "frame2": None, 'frame3': None, 'frame4': None}

    # Default parameters
    # sde_parameters = {"data": "data", "requests": "requests", "outputs": "outputs", "logging": "logging",
    #                   "bootstrap_servers": "parallelization": "2",
    #                   "syn_filename": "synopses.txt",
    #                   "dataset_filename": "datasets.txt"}

    def __init__(self):
        super().__init__()

        # Paths
        self.kafka_path = "/home/wieger/Desktop/Programs/kafka_2.11-2.2.0/"
        self.credentials = load_credentials('credentials.json')
        # Buttons
        self.bt_start_sde = None
        self.seg_button = None
        self.btSynFilename = None

        # Entries
        self.bootstrap_servers = None
        self.data_topic = None
        self.request_topic = None
        self.output_topic = None
        self.logging_topic = None
        self.parallelization = None
        self.synFileName = None

        self.existing_synopses = {}
        self.existing_datasets = read_metainfo_existing_datasets()

        self.dsMap = DatasetMap.getDatasetMap(DatasetMap())
        self.u_nameToUID = {}

        # Window settings
        self.title("STELAR Synopsis Data Engine")
        self.geometry("{0}x{0}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))

        # contains everything
        main_container = customtkinter.CTkFrame(self)
        main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        # buttons to select the frames
        self.seg_button = customtkinter.CTkSegmentedButton(main_container, command=self.frame_selector)
        self.seg_button.pack(side=tkinter.TOP, fill=tkinter.X, expand=False, padx=10, pady=10)
        self.seg_button.configure(
            values=["Dataset Management", "Create Synopsis", "Query Synopsis", "Query Spatial Synopsis"])

        # left side panel -> for frame selection
        left_side_panel = customtkinter.CTkFrame(main_container, width=100)
        self.set_left_side_panel(left_side_panel)

        # right side panel -> to show the frame1 or frame 2
        self.right_side_panel = customtkinter.CTkFrame(main_container)
        self.right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        self.right_side_container = customtkinter.CTkFrame(self.right_side_panel, fg_color="#000811")
        self.right_side_container.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

        App.frames['frame1'] = customtkinter.CTkFrame(main_container)
        App.frames['frame2'] = customtkinter.CTkFrame(main_container)
        App.frames['frame3'] = customtkinter.CTkFrame(main_container)
        App.frames['frame4'] = customtkinter.CTkFrame(main_container)

        self.frame1 = DataManagement(self)
        self.frame1.set_frame1()
        self.frame2 = CreateSynFrame(self)
        self.frame3 = QueryNormal(self)
        self.frame4 = QuerySpatial(self)

        self.sde_parameters = {"data_topic": "data", "request_topic": "requests",
                               "output_topic": "outputs", "logging_topic": "logging",
                               "bootstrap_servers": self.credentials["kafka"]["bootstrap_servers"],
                               "parallelization": "2", "syn_filename": "synopses.txt",
                               "dataset_filename": "datasets.txt"}

        self.sde = Client("sde.petrounetwork.gr:19092", message_queue_size=20, response_timeout=10)
        self.sde.send_storage_auth_request(self.credentials["klms"]["access_key"], self.credentials["klms"]["secret_key"],self.credentials["klms"]["session_token"], self.credentials["klms"]["endpoint"])

        self.stelar_client = stelarClient(base_url=self.credentials['stelar_client']['url'],
                                    username=self.credentials['stelar_client']['username'],
                                    password=self.credentials['stelar_client']['password'])

        # Selected dataset from MINIO
        self.selected_dataset = None
        self.current_dataset = None


    def set_sde_par_panel(self, sde_par_panel):
        label_kafka = customtkinter.CTkLabel(sde_par_panel, text="SDE Parameters",
                                             font=customtkinter.CTkFont(size=13, weight="bold"))
        label_kafka.grid(row=0, padx=(10, 20), pady=10, columnspan=2)

        label_data_topic = customtkinter.CTkLabel(sde_par_panel, text="Data Topic",
                                                  font=customtkinter.CTkFont(size=13, weight="bold"))
        label_data_topic.grid(row=1, column=0, padx=(20, 10), pady=10)
        data_text = customtkinter.StringVar(value="data_topic")
        self.data_topic = customtkinter.CTkEntry(sde_par_panel, placeholder_text="data_topic", textvariable=data_text)
        self.data_topic.grid(row=1, column=1, padx=(10, 20), pady=10)

        label_request_topic = customtkinter.CTkLabel(sde_par_panel, text="Request Topic",
                                                     font=customtkinter.CTkFont(size=13, weight="bold"))
        label_request_topic.grid(row=2, column=0, padx=(20, 10), pady=10)
        req_text = customtkinter.StringVar(value="requests")
        self.request_topic = customtkinter.CTkEntry(sde_par_panel, placeholder_text="requests", textvariable=req_text)
        self.request_topic.grid(row=2, column=1, padx=(10, 20), pady=10)

        label_OUT = customtkinter.CTkLabel(sde_par_panel, text="Output Topic",
                                           font=customtkinter.CTkFont(size=13, weight="bold"))
        label_OUT.grid(row=3, column=0, padx=(20, 10), pady=10)
        out_text = customtkinter.StringVar(value="outputs")
        self.output_topic = customtkinter.CTkEntry(sde_par_panel, placeholder_text="outputs", textvariable=out_text)
        self.output_topic.grid(row=3, column=1, padx=(10, 20), pady=10)

        label_logging = customtkinter.CTkLabel(sde_par_panel, text="logging",
                                           font=customtkinter.CTkFont(size=13, weight="bold"))
        label_logging.grid(row=4, column=0, padx=(20, 10), pady=10)
        logging_text = customtkinter.StringVar(value="logging")
        self.logging_topic = customtkinter.CTkEntry(sde_par_panel, placeholder_text="logging", textvariable=logging_text)
        self.logging_topic.grid(row=4, column=1, padx=(10, 20), pady=10)

        label_bootstrap = customtkinter.CTkLabel(sde_par_panel, text="Bootstrap Servers",
                                                 font=customtkinter.CTkFont(size=13, weight="bold"))
        label_bootstrap.grid(row=5, column=0, padx=(20, 10), pady=10)
        bs_text = customtkinter.StringVar(value=self.credentials["kafka"]["bootstrap_servers"])
        self.bootstrap_servers = customtkinter.CTkEntry(sde_par_panel, placeholder_text=self.credentials["kafka"]["bootstrap_servers"], textvariable=bs_text)
        self.bootstrap_servers.grid(row=5, column=1, padx=(10, 20), pady=10)

        label_par = customtkinter.CTkLabel(sde_par_panel, text="Parallelization",
                                           font=customtkinter.CTkFont(size=13, weight="bold"))
        label_par.grid(row=6, column=0, padx=(20, 10), pady=10)
        par_text = customtkinter.StringVar(value="2")
        self.parallelization = customtkinter.CTkEntry(sde_par_panel, placeholder_text="2", textvariable=par_text)
        self.parallelization.grid(row=6, column=1, padx=(10, 20), pady=10)

        # filename of existing synopses
        # label_filename = customtkinter.CTkLabel(sde_par_panel, text="Filename Synopses",
        #                                         font=customtkinter.CTkFont(size=13, weight="bold"))
        # label_filename.grid(row=6, column=0, padx=(20, 10), pady=10)
        # self.btSynFilename = customtkinter.CTkEntry(sde_par_panel, placeholder_text="synopsis.txt")
        # self.btSynFilename.grid(row=6, column=1, padx=(10, 20), pady=10)

        # create button to save the parameters
        bt_save = customtkinter.CTkButton(sde_par_panel, text="Connect to running SDE", command=self.save_parameters)
        bt_save.grid(row=7, column=0, columnspan=2, padx=(20, 10), pady=10)

        self.bt_start_sde = customtkinter.CTkButton(sde_par_panel, text="Manually start SDE", command=self.start_sde)
        self.bt_start_sde.grid(row=8, column=0, columnspan=2, padx=(20, 10), pady=10)

    def save_parameters(self):
        if self.data_topic.get() == "":
            self.sde_parameters["data_topic"] = "data"
        else:
            self.sde_parameters["data_topic"] = self.data_topic.get()
        if self.request_topic.get() == "":
            self.sde_parameters["request_topic"] = "requests"
        else:
            self.sde_parameters["request_topic"] = self.request_topic.get()
        if self.output_topic.get() == "":
            self.sde_parameters["output_topic"] = "outputs"
        else:
            self.sde_parameters["output_topic"] = self.output_topic.get()
        if self.logging_topic.get() == "":
            self.sde_parameters["logging_topic"] = "logging"
        else:
            self.sde_parameters["logging_topic"] = self.logging_topic.get()
        if self.bootstrap_servers.get() == "":
            # self.sde_parameters["bootstrap_servers"] = "localhost:9092"
            self.sde_parameters["bootstrap_servers"] = self.credentials["kafka"]["bootstrap_servers"]
        else:
            self.sde_parameters["bootstrap_servers"] = self.bootstrap_servers.get()
        if self.parallelization.get() == "":
            self.sde_parameters["parallelization"] = "2"
        else:
            self.sde_parameters["parallelization"] = self.parallelization.get()
        # if self.btSynFilename.get() == "":
        self.sde_parameters["syn_filename"] = "synopses.txt"
        # else:
        #     self.sde_parameters["syn_filename"] = self.btSynFilename.get()

    def start_sde(self):
        self.save_parameters()
        # Disable the button to prevent multiple clicks
        self.bt_start_sde.configure(state=customtkinter.DISABLED)

        # Start the subprocess in a separate thread
        thread = threading.Thread(target=self.run_bash_script)
        thread.start()

    def run_bash_script(self):
        try:
            # start the SDE
            subprocess.check_call([self.kafka_path + 'sde_start_wp.sh',
                                   self.sde_parameters["data_topic"], self.sde_parameters["request_topic"],
                                   self.sde_parameters["output_topic"], self.sde_parameters["bootstrap_servers"],
                                   self.sde_parameters["parallelization"],
                                   os.path.dirname(os.path.realpath(__file__)) + "/" + self.sde_parameters["syn_filename"]])
        except subprocess.CalledProcessError as e:
            messagebox.showinfo("Error", "Error starting SDE", parent=self.frame)
        finally:
            self.bt_start_sde.configure(state=customtkinter.NORMAL)

    def set_left_side_panel(self, left_side_panel):
        left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=10, pady=10)

        # create grid in leftside panel for kafka topics, filename of existing synopses
        sde_par_panel = customtkinter.CTkFrame(left_side_panel, width=100)
        sde_par_panel.grid(row=4, column=0, padx=(20, 10), pady=(50, 10))
        self.set_sde_par_panel(sde_par_panel)
        # image of stelar
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        img = Image.open(os.path.join(image_path, "Logo - Stelar project.jpg"))
        # img = ImageOps.fit(img, (self.desiredSize, self.desiredSize))
        img_width, img_height = img.size
        stelar_img = customtkinter.CTkImage(img, size=(img_width, img_height))
        label_image = customtkinter.CTkLabel(left_side_panel, text="", image=stelar_img)
        label_image.image = stelar_img
        label_image.grid(row=5, padx=(10, 20), pady=300, columnspan=2)

    def frame_selector(self, value):
        frame_number = 1
        if value == "Dataset Management":
            frame_number = 1
        elif value == "Create Synopsis":
            frame_number = 2
            self.frame2.set_frame2()
        elif value == "Query Synopsis":
            frame_number = 3
            self.frame3.set_frame3()
        elif value == "Query Spatial Synopsis":
            frame_number = 4
            self.frame4.set_frame4()

        for i in range(1, num_frames + 1):
            if i == frame_number:
                App.frames[f"frame{i}"].pack(in_=self.right_side_container,side=tkinter.TOP, fill=tkinter.BOTH,
                                             expand=True, padx=0, pady=0)
            else:
                App.frames[f"frame{i}"].pack_forget()

    def read_syns_from_sde(self, dataset_key):
        if dataset_key is None:
            # warning: no dataset selected
            messagebox.showinfo("No dataset selected", "Select dataset to load synopses.", parent=self.frame)
        req = {
            "key": dataset_key,
            "streamID": "S1",
            "synopsisID": 1,
            "requestID": 777,
            "dataSetkey": dataset_key,
            "param": ["synopses"],
            "noOfP": int(self.parallelization.get()),
            "uid": 5,
            "externalUID": "getListOfsynopses"
        }
        resp = self.sde.send_request(req, "getListOfsynopses")
        if resp is None:
            messagebox.showinfo("Error", "Error loading synopses.", parent=self.frame)
        print("Resp: ", resp)
        synopses = extract_json_from_content(resp)
        for syn in synopses:
            print(syn)
            self.existing_synopses[syn["externalUID"]] = syn

    # def read_datasets_from_file(self):
        # if os.path.isfile(self.sde_parameters["dataset_filename"]):
        #     with open(self.sde_parameters["dataset_filename"], "r") as file:
        #         for line in file:
        #             dataset = DataManagement.readDataset(line)
        #             self.existing_datasets[dataset['DatasetKey']] = dataset


if __name__ == "__main__":
    app = App()
    app.mainloop()