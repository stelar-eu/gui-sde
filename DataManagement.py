from tkinter import messagebox

import customtkinter

from DataClient import DataClient
from ScrollableRadioButtonFrame import ScrollableRadiobuttonFrame


class DataManagement:
    def __init__(self, app):
        self.bt_load_datasets = None
        self.bt_refresh = None
        self.App = app
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

    def load_datasets(self):
        datasets = self.App.stelar_client.datasets[:]
        shown_datasets = []
        for dataset in datasets:
            if dataset.name in self.App.existing_datasets:
                shown_datasets.append(dataset)

        self.scrollable_frame = ScrollableRadiobuttonFrame(master=self.frame,
                                                           item_list=shown_datasets,
                                                           label_text="Select Dataset", width=1000,
                                                           height=500, fg_color="#000811", command=self.select_dataset)
        self.scrollable_frame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        if self.bt_load_datasets:
            self.bt_load_datasets.destroy()
        if self.bt_refresh:
            self.bt_refresh.destroy()

        self.bt_refresh = customtkinter.CTkButton(master=self.frame, text="Refresh",
                                                  command=self.load_datasets)
        self.bt_refresh.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)


    def select_dataset(self):
        self.App.selected_dataset = self.scrollable_frame.get_checked_item()
        if self.App.selected_dataset:
            # now look in self.App.existing_datasets for the selected dataset
            if self.App.selected_dataset.name in self.App.existing_datasets:
                self.App.current_dataset = self.App.existing_datasets[self.App.selected_dataset.name]
            else:
                # Need to add dataset to existing datasets
                messagebox.showinfo("Error", f"Dataset {self.App.selected_dataset.name} not found in existing datasets")
        messagebox.showinfo("Selected Dataset", f"Selected Dataset: {self.App.selected_dataset.name}")



