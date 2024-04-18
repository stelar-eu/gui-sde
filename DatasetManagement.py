import ast
from tkinter import messagebox

import customtkinter

from ScrollableRadioButtonFrame import ScrollableRadiobuttonFrame


class DatasetManagement:
    def __init__(self, App):
        # self.select_dataset = None
        self.App = App

        # buttons
        self.bt_load_datasets = None
        self.bt_add_dataset = None

        # Text entry
        self.entry_dataset_name = None

        # copy synopsis frame
        self.frame = self.App.frames["frame1"]

        # Frame
        self.new_dataset_frame = None

        # Dataset specific
        self.minX = None
        self.maxX = None
        self.minY = None
        self.maxY = None
        self.maxResolution = None
        self.parameters = None

    def set_frame1(self):
        self.frame = self.App.frames["frame1"]
        # set title
        title = customtkinter.CTkLabel(self.frame, text="Dataset Management",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        title.place(relx=0.5, rely=0.02, anchor=customtkinter.CENTER)

        # label_dataset_name = customtkinter.CTkLabel(self.frame, text="Dataset Filename",
        #                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        # label_dataset_name.place(relx=0.25, rely=0.2, anchor=customtkinter.CENTER)
        # self.entry_dataset_name = customtkinter.CTkEntry(master=self.frame, width=250, placeholder_text="dataset.txt")
        # self.entry_dataset_name.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)


        # select dataset name from list
        self.bt_load_datasets = customtkinter.CTkButton(master=self.frame, text="Load Datasets",
                                                        command=self.load_datasets)
        self.bt_load_datasets.place(relx=0.75, rely=0.2, anchor=customtkinter.CENTER)

        self.new_dataset()

    def load_datasets(self):
        self.App.dataset_filename = "dataset.txt"

        self.App.read_datasets_from_file()

        self.scrollable_frame = ScrollableRadiobuttonFrame(master=self.frame,
                                                           item_list=self.App.existing_datasets,
                                                           label_text="Select Dataset", width=650,
                                                           height=400, fg_color="#000811", command=self.select_dataset)
        self.scrollable_frame.place(relx=0.75, rely=0.5, anchor=customtkinter.CENTER)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.reload_existing_datasets()

    def reload_existing_datasets(self):
        self.App.current_dataset = None
        if self.scrollable_frame is not None:
            self.scrollable_frame.delete_all_items()
        for DatasetKey in self.App.existing_datasets:
            self.scrollable_frame.add_item_dataset(self.App.existing_datasets[DatasetKey])

    @classmethod
    def readDataset(cls, line):
        dataset = ast.literal_eval(line)
        # dataset = {}
        # dataset["DatasetKey"] = dataset_list[0]
        # dataset["DatasetName"] = dataset_list[1]
        # dataset["StreamID"] = dataset_list[2]
        # dataset["path"] = dataset_list[3]
        # dataset["minX"] = dataset_list[4]
        # dataset["maxX"] = dataset_list[5]
        # dataset["minY"] = dataset_list[6]
        # dataset["maxY"] = dataset_list[7]
        return dataset

    def new_dataset(self):
        self.new_dataset_frame = customtkinter.CTkFrame(self.frame, width=200, height=250, fg_color="#000811")
        self.new_dataset_frame.place(relx=0.25, rely=0.5, anchor=customtkinter.CENTER)

        label_add_new_dataset = customtkinter.CTkLabel(self.new_dataset_frame, text="Add New Dataset",
                                                       font=customtkinter.CTkFont(size=15, weight="bold"))
        label_add_new_dataset.grid(row=0, columnspan=2, padx=20, pady=(10, 10), sticky="nsew")

        label_dataset_key = customtkinter.CTkLabel(self.new_dataset_frame, text="DatasetKey",
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        label_dataset_key.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.entry_dataset_key = customtkinter.CTkEntry(master=self.new_dataset_frame, width=250, placeholder_text="D1")
        self.entry_dataset_key.grid(row=1, column=1, padx=(20, 20), pady=(20, 20))

        label_dataset_name = customtkinter.CTkLabel(self.new_dataset_frame, text="Dataset Name",
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        label_dataset_name.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")

        self.entry_dataset_name = customtkinter.CTkEntry(master=self.new_dataset_frame, width=250, placeholder_text="Weather")
        self.entry_dataset_name.grid(row=2, column=1, padx=(20, 20), pady=(20, 20))

        label_stream_id = customtkinter.CTkLabel(self.new_dataset_frame, text="Stream ID",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        label_stream_id.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.entry_stream_id = customtkinter.CTkEntry(master=self.new_dataset_frame, width=250, placeholder_text="S1")
        self.entry_stream_id.grid(row=3, column=1, padx=(20, 20), pady=(20, 20))

        bt_add_dataset = customtkinter.CTkButton(master=self.new_dataset_frame, text="Add Dataset",
                                                 command=self.add_dataset)
        bt_add_dataset.grid(row=5, columnspan=2, padx=(20, 0), pady=(20, 20))

    def add_dataset(self):
        self.minX = None
        self.maxX = None
        self.minY = None
        self.maxY = None
        self.maxResolution = None

        dataset = {}
        dataset["DatasetKey"] = self.entry_dataset_key.get()
        dataset["DatasetName"] = self.entry_dataset_name.get()
        dataset["StreamID"] = self.entry_stream_id.get()

        # if dataset["DatasetName"] == "Weather":
        if dataset["DatasetName"] in self.App.dsMap:
            self.load_coordinates_dataset(dataset["DatasetName"])


        dataset["minX"] = self.minX
        dataset["maxX"] = self.maxX
        dataset["minY"] = self.minY
        dataset["maxY"] = self.maxY
        dataset["maxResolution"] = self.maxResolution
        dataset["parameters"] = self.parameters

        self.App.add_dataset_to_existing(dataset)

        messagebox.showinfo("Info", "Dataset added successfully", master=self.new_dataset_frame)

    def load_coordinates_dataset(self, name):
        self.minX = self.App.dsMap[name]["minX"]
        self.maxX = self.App.dsMap[name]["maxX"]
        self.minY = self.App.dsMap[name]["minY"]
        self.maxY = self.App.dsMap[name]["maxY"]
        self.maxResolution = self.App.dsMap[name]["maxResolution"]
        self.parameters = self.App.dsMap[name]["parameters"]
        # self.minX = -100000
        # self.maxX = 350000
        # self.minY = 350000
        # self.maxY = 650000
        # self.maxResolution = 128

    def select_dataset(self):
        self.App.current_dataset = self.scrollable_frame.get_checked_item()