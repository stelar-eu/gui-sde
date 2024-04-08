import customtkinter
import ast

class ScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        text = ("Unique ID: {}\n"
                "Synopsis ID: {}\n"
                "Dataset: {} \n"
                "Stream ID: {} \n"
                "Number of Parallelization: {} \n"
                "Synopsis specific parameters: {}").format(
                                                      item['uid'],
                                                      item['synopsisID'],
                                                      item['dataSetkey'], item['streamID'],
                                                      item['noOfP'],
                                                      item['param'])

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
