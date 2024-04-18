import customtkinter
import ast

from datasetMap import DatasetMap
from synMap import SynMap


class ScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []
        print("item_list", item_list)
        for i, item in enumerate(item_list):
            if 'u_name' in item:
                self.add_item(item)
            else:
                self.add_item_dataset(item_list[item])

    def add_item(self, item):
        print("item", item)
        print(SynMap.getSynName(SynMap(), int(item['synopsisID'])))
        text = ("Unique Name: {}\n"
                "Synopsis Type: {}\n"
                "Dataset: {} \n"
                "Stream ID: {} \n"
                "Number of Parallelization: {} \n"
                "Synopsis specific parameters: {}").format(
                                                      item['u_name'],
                                                      SynMap.getSynName(SynMap(), int(item['synopsisID'])),
                                                      item['dataSetkey'], item['streamID'],
                                                      item['noOfP'],
                                                      item['param'])

        radiobutton = customtkinter.CTkRadioButton(self, text=text, value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(0, 10))
        self.radiobutton_list.append(radiobutton)

    def add_item_dataset(self, item):
        print(item)
        text = ("DatasetKey: {}\n"
                "Dataset: {} \n"
                "Stream ID: {} \n").format(item['DatasetKey'],item['DatasetName'], item['StreamID'])
        if item['minX'] is not None:
            text += "MinX: {} \n".format(item['minX'])
            text += "MaxX: {} \n".format(item['maxX'])
            text += "MinY: {} \n".format(item['minY'])
            text += "MaxY: {} \n".format(item['maxY'])
            text += "Max Resolution: {} \n".format(item['maxResolution'])

        radiobutton = customtkinter.CTkRadioButton(self, text=text, value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(0, 10))
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return

    def get_checked_item(self):
        itemString = self.radiobutton_variable.get()
        item = ast.literal_eval(itemString)
        return item


    def delete_all_items(self):
        for radiobutton in self.radiobutton_list:
            radiobutton.destroy()
        self.radiobutton_list = []
