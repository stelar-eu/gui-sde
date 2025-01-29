from tkinter import messagebox

import customtkinter

from RRDatasetSender import RRDatasetSender
from ScrollableRadioButtonFrame import ScrollableRadiobuttonFrame
from MinIOClient import MinIOClient

class DataManagement:
    def __init__(self, App):
        self.App = App
        self.minio_client = MinIOClient(bucket_name="sde-bucket", credentials=self.App.credentials)
        self.selected_dataset = None
        self.frame = self.App.frames["frame1"]
        self.scrollable_frame = None

    def set_frame1(self):
        self.frame = self.App.frames["frame1"]
        title = customtkinter.CTkLabel(self.frame, text="Dataset Management",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        title.place(relx=0.5, rely=0.02, anchor=customtkinter.CENTER)

        self.bt_load_datasets = customtkinter.CTkButton(master=self.frame, text="Load Datasets",
                                                        command=self.load_datasets)
        self.bt_load_datasets.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self.bt_refresh = customtkinter.CTkButton(master=self.frame, text="Refresh",
                                                    command=self.load_datasets)
        self.bt_refresh.place(relx=0.6, rely=0.5, anchor=customtkinter.CENTER)
    def load_datasets(self):
        datasets = self.minio_client.list_files()
        self.scrollable_frame = ScrollableRadiobuttonFrame(master=self.frame,
                                                           item_list=datasets,
                                                           label_text="Select Dataset", width=1000,
                                                           height=750, fg_color="#000811", command=self.select_dataset)
        self.scrollable_frame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.bt_load_selected_dataset = customtkinter.CTkButton(master=self.frame, text="Load Selected Dataset",
                                                                command=self.load_selected_dataset)
        self.bt_load_selected_dataset.place(relx=0.5, rely=0.8, anchor=customtkinter.CENTER)

    def select_dataset(self):
        self.selected_dataset = self.scrollable_frame.get_checked_item()

    def load_selected_dataset(self):
        if self.selected_dataset:
            data = self.minio_client.load_file(self.selected_dataset)
            rr = RRDatasetSender(data, self.App)
            rr.send()
            messagebox.showinfo("Info", "All data has been sent to the Kafka topic", master=self.frame)

    def send_record_to_kafka(self, record):
        # Implement the logic to send the record to Kafka using messages.Datapoint.py


        print(record)