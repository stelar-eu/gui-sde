import ast
import os
import threading
import tkinter
import tkinter.messagebox
from tkinter import messagebox

import customtkinter

import subprocess
from customtkinter import CTk

from CreateSynFrame import CreateSynFrame
from QueryNormal import QueryNormal
from QuerySpatial import QuerySpatial
from DatasetManagement import DatasetManagement
from datasetMap import DatasetMap

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


class App(customtkinter.CTk):
    frames = {"frame1": None, "frame2": None, 'frame3': None, 'frame4': None}

    # Default parameters
    sde_parameters = {"data_topic": "data_topic", "request_topic": "request_topic", "OUT": "OUT",
                      "bootstrap_servers": "localhost:9092", "parallelization": "16",
                      "syn_filename": "synopses.txt",
                      "dataset_filename": "datasets.txt"}

    def __init__(self):
        super().__init__()

        # Paths
        self.kafka_path = "/home/wieger/Desktop/Programs/kafka_2.11-2.2.0/"

        # Buttons
        self.bt_start_sde = None
        self.seg_button = None
        self.btSynFilename = None

        # Entries
        self.bootstrap_servers = None
        self.data_topic = None
        self.request_topic = None
        self.OUT = None
        self.parallelization = None
        self.synFileName = None

        self.existing_synopses = {}
        self.existing_datasets = {}

        self.current_dataset = None
        self.dsMap = DatasetMap.getDatasetMap(DatasetMap())
        self.u_nameToUID = {}

        # Window settings
        self.title("Synopsis Data Engine")
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

        self.frame1 = DatasetManagement(self)
        self.frame1.set_frame1()
        self.frame2 = CreateSynFrame(self)
        self.frame3 = QueryNormal(self)
        self.frame4 = QuerySpatial(self)

    def set_sde_par_panel(self, sde_par_panel):
        label_kafka = customtkinter.CTkLabel(sde_par_panel, text="SDE Parameters",
                                             font=customtkinter.CTkFont(size=13, weight="bold"))
        label_kafka.grid(row=0, padx=(10, 20), pady=10, columnspan=2)

        label_data_topic = customtkinter.CTkLabel(sde_par_panel, text="Data Topic",
                                                  font=customtkinter.CTkFont(size=13, weight="bold"))
        label_data_topic.grid(row=1, column=0, padx=(20, 10), pady=10)
        self.data_topic = customtkinter.CTkEntry(sde_par_panel, placeholder_text="data_topic")
        self.data_topic.grid(row=1, column=1, padx=(10, 20), pady=10)

        label_request_topic = customtkinter.CTkLabel(sde_par_panel, text="Request Topic",
                                                     font=customtkinter.CTkFont(size=13, weight="bold"))
        label_request_topic.grid(row=2, column=0, padx=(20, 10), pady=10)
        self.request_topic = customtkinter.CTkEntry(sde_par_panel, placeholder_text="request_topic")
        self.request_topic.grid(row=2, column=1, padx=(10, 20), pady=10)

        label_OUT = customtkinter.CTkLabel(sde_par_panel, text="OUT",
                                           font=customtkinter.CTkFont(size=13, weight="bold"))
        label_OUT.grid(row=3, column=0, padx=(20, 10), pady=10)
        self.OUT = customtkinter.CTkEntry(sde_par_panel, placeholder_text="OUT")
        self.OUT.grid(row=3, column=1, padx=(10, 20), pady=10)

        label_bootstrap = customtkinter.CTkLabel(sde_par_panel, text="Bootstrap Servers",
                                                 font=customtkinter.CTkFont(size=13, weight="bold"))
        label_bootstrap.grid(row=4, column=0, padx=(20, 10), pady=10)
        self.bootstrap_servers = customtkinter.CTkEntry(sde_par_panel, placeholder_text="localhost:9092")
        self.bootstrap_servers.grid(row=4, column=1, padx=(10, 20), pady=10)

        label_par = customtkinter.CTkLabel(sde_par_panel, text="Parallelization",
                                           font=customtkinter.CTkFont(size=13, weight="bold"))
        label_par.grid(row=5, column=0, padx=(20, 10), pady=10)
        self.parallelization = customtkinter.CTkEntry(sde_par_panel, placeholder_text="16")
        self.parallelization.grid(row=5, column=1, padx=(10, 20), pady=10)

        # filename of existing synopses
        # label_filename = customtkinter.CTkLabel(sde_par_panel, text="Filename Synopses",
        #                                         font=customtkinter.CTkFont(size=13, weight="bold"))
        # label_filename.grid(row=6, column=0, padx=(20, 10), pady=10)
        # self.btSynFilename = customtkinter.CTkEntry(sde_par_panel, placeholder_text="synopsis.txt")
        # self.btSynFilename.grid(row=6, column=1, padx=(10, 20), pady=10)

        # create button to save the parameters
        bt_save = customtkinter.CTkButton(sde_par_panel, text="Connect to running SDE", command=self.save_parameters)
        bt_save.grid(row=6, column=0, columnspan=2, padx=(20, 10), pady=10)

        self.bt_start_sde = customtkinter.CTkButton(sde_par_panel, text="Manually start SDE", command=self.start_sde)
        self.bt_start_sde.grid(row=7, column=0, columnspan=2, padx=(20, 10), pady=10)

    def save_parameters(self):
        if self.data_topic.get() == "":
            self.sde_parameters["data_topic"] = "data_topic"
        else:
            self.sde_parameters["data_topic"] = self.data_topic.get()
        if self.request_topic.get() == "":
            self.sde_parameters["request_topic"] = "request_topic"
        else:
            self.sde_parameters["request_topic"] = self.request_topic.get()

        if self.OUT.get() == "":
            self.sde_parameters["OUT"] = "OUT"
        else:
            self.sde_parameters["OUT"] = self.OUT.get()
        if self.bootstrap_servers.get() == "":
            self.sde_parameters["bootstrap_servers"] = "localhost:9092"
        else:
            self.sde_parameters["bootstrap_servers"] = self.bootstrap_servers.get()
        if self.parallelization.get() == "":
            self.sde_parameters["parallelization"] = "16"
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
                                   self.sde_parameters["OUT"], self.sde_parameters["bootstrap_servers"],
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

    def add_synopsis(self, request):
        self.existing_synopses[request["u_name"]] = request
        add_to_file(request, self.sde_parameters["syn_filename"])

    def add_dataset_to_existing(self, dataset):
        self.existing_datasets[dataset["DatasetKey"]] = dataset
        add_to_file(dataset, self.sde_parameters["dataset_filename"])

    def delete_synopsis(self, request):
        if request["u_name"] in self.existing_synopses:
            del self.existing_synopses[request["u_name"]]
        else:
            messagebox.showinfo("Error", "Synopsis not found", parent=self.frame)

    def read_syns_from_file(self):
        if os.path.isfile(self.sde_parameters["syn_filename"]):
            with open(self.sde_parameters["syn_filename"], "r") as file:
                for line in file:
                    print(line)
                    request = ast.literal_eval(line)
                    self.existing_synopses[request["u_name"]] = request

    def read_datasets_from_file(self):
        if os.path.isfile(self.sde_parameters["dataset_filename"]):
            with open(self.sde_parameters["dataset_filename"], "r") as file:
                for line in file:
                    dataset = DatasetManagement.readDataset(line)
                    self.existing_datasets[dataset['DatasetKey']] = dataset


if __name__ == "__main__":
    app = App()
    app.mainloop()