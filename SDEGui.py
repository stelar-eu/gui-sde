import os
import tkinter
import tkinter.messagebox
from tkinter import messagebox

import customtkinter
from customtkinter import CTk

from CreateSynFrame import CreateSynFrame
from QueryNormal import QueryNormal
from QuerySpatial import QuerySpatial

from messages.Request import Request


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

num_frames = 4
#"data_topic" "request_topic" "OUT" "localhost:9092" "2"

def setFrame1(main_container):
    App.frames['frame1'] = customtkinter.CTkFrame(main_container)
    bt_from_frame1 = customtkinter.CTkButton(App.frames['frame1'], text="Test 1", command=lambda: print("test 1"))
    bt_from_frame1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    return main_container


def setFrame4(main_container):
    App.frames['frame4'] = customtkinter.CTkFrame(main_container)
    bt_from_frame4 = customtkinter.CTkButton(App.frames['frame4'], text="Test 4", command=lambda: print("test 4"))
    bt_from_frame4.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    return main_container




class App(customtkinter.CTk):
    frames = {"frame1": None, "frame2": None, 'frame3': None, 'frame4': None}

    sde_parameters = {"data_topic": "data_topic", "request_topic": "request_topic", "OUT": "OUT",
                      "bootstrap_servers": "localhost:9092", "parallelization": "2", "filename": "synopses.txt"}

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
        self.parallelization = customtkinter.CTkEntry(sde_par_panel, placeholder_text="2")
        self.parallelization.grid(row=5, column=1, padx=(10, 20), pady=10)

        # filename of existing synopses
        label_filename = customtkinter.CTkLabel(sde_par_panel, text="Filename Synopses",
                                                font=customtkinter.CTkFont(size=13, weight="bold"))
        label_filename.grid(row=6, column=0, padx=(20, 10), pady=10)
        self.btSynFilename = customtkinter.CTkEntry(sde_par_panel, placeholder_text="filename")
        self.btSynFilename.grid(row=6, column=1, padx=(10, 20), pady=10)

        # create button to save the parameters
        bt_save = customtkinter.CTkButton(sde_par_panel, text="Save", command=self.save_parameters)
        bt_save.grid(row=7, column=0, columnspan=2, padx=(20, 10), pady=10)

    def save_parameters(self):
        if (self.data_topic.get() == ""):
            self.sde_parameters["data_topic"] = "data_topic"
        else:
            self.sde_parameters["data_topic"] = self.data_topic.get()
        if (self.request_topic.get() == ""):
            self.sde_parameters["request_topic"] = "request_topic"
        else:
            self.sde_parameters["request_topic"] = self.request_topic.get()

        if (self.OUT.get() == ""):
            self.sde_parameters["OUT"] = "OUT"
        else:
            self.sde_parameters["OUT"] = self.OUT.get()
        if (self.bootstrap_servers.get() == ""):
            self.sde_parameters["bootstrap_servers"] = "localhost:9092"
        else:
            self.sde_parameters["bootstrap_servers"] = self.bootstrap_servers.get()
        if (self.parallelization.get() == ""):
            self.sde_parameters["parallelization"] = "2"
        else:
            self.sde_parameters["parallelization"] = self.parallelization.get()
        if (self.btSynFilename.get() == ""):
            self.sde_parameters["filename"] = "synopses.txt"
        else:
            self.sde_parameters["filename"] = self.btSynFilename.get()
        # if file does not exist, create it
        #self.init_syn_file()
    def set_left_side_panel(self, left_side_panel):
        left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=10, pady=10)





        #bt_frame1 = customtkinter.CTkButton(left_side_panel, text="Dataset Management", command=self.frame1_selector)
        # bt_frame1.grid(row=0, column=0, padx=20, pady=10)
        # 
        # bt_frame2 = customtkinter.CTkButton(left_side_panel, text="Create Synopsis", command=self.frame2_selector)
        # bt_frame2.grid(row=1, column=0, padx=20, pady=10)
        # 
        # bt_frame3 = customtkinter.CTkButton(left_side_panel, text="Query Synopsis", command=self.frame3_selector)
        # bt_frame3.grid(row=2, column=0, padx=20, pady=10)
        # 
        # bt_frame4 = customtkinter.CTkButton(left_side_panel, text="Query Spatial Synopsis",
        #                                     command=self.frame4_selector)
        # bt_frame4.grid(row=3, column=0, padx=20, pady=10)

        # create grid in leftside panel for kafka topics, filename of existing synopses
        sde_par_panel = customtkinter.CTkFrame(left_side_panel, width=100)
        sde_par_panel.grid(row=4, column=0, padx=(20, 10), pady=(50, 10))
        self.set_sde_par_panel(sde_par_panel)

    def frame1_selector(self):
        App.frames["frame2"].pack_forget()
        App.frames["frame3"].pack_forget()
        App.frames["frame4"].pack_forget()
        App.frames["frame1"].pack(in_=self.right_side_container,side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

    def frame_selector(self, value):
        frame_number = 1
        if value == "Dataset Management":
            frame_number = 1
        elif value == "Create Synopsis":
            frame_number = 2
        elif value == "Query Synopsis":
            frame_number = 3
        elif value == "Query Spatial Synopsis":
            frame_number = 4

        for i in range(1, num_frames + 1):
            if i == frame_number:
                App.frames[f"frame{i}"].pack(in_=self.right_side_container,side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
            else:
                App.frames[f"frame{i}"].pack_forget()
        # App.frames["frame2"].pack_forget()
        # App.frames["frame3"].pack_forget()
        # App.frames["frame4"].pack_forget()
        # App.frames["frame1"].pack(in_=self.right_side_container,side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

    def frame2_selector(self):
        App.frames["frame1"].pack_forget()
        App.frames["frame3"].pack_forget()
        App.frames["frame4"].pack_forget()
        App.frames["frame2"].pack(in_=self.right_side_container,side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

    def frame3_selector(self):
        App.frames["frame1"].pack_forget()
        App.frames["frame2"].pack_forget()
        App.frames["frame4"].pack_forget()
        App.frames["frame3"].pack(in_=self.right_side_container, side=tkinter.TOP, fill=tkinter.BOTH, expand=True,
                                  padx=0, pady=0)

    def frame4_selector(self):
        App.frames["frame1"].pack_forget()
        App.frames["frame2"].pack_forget()
        App.frames["frame3"].pack_forget()
        App.frames["frame4"].pack(in_=self.right_side_container, side=tkinter.TOP, fill=tkinter.BOTH, expand=True,
                                  padx=0, pady=0)

    def add_synopsis(self, request):
        self.existing_synopses[request["uid"]] = request
        self.add_syn_to_file(request)

    def delete_synopsis(self, request):
        if request["uid"] in self.existing_synopses:
            del self.existing_synopses[request["uid"]]
        else:
            messagebox.showinfo("Error", "Synopsis not found", parent=self.frame)

    def __init__(self):
        super().__init__()
        # self.state('withdraw')
        self.seg_button = None
        self.bootstrap_servers = None
        self.data_topic = None
        self.request_topic = None
        self.OUT = None
        self.parallelization = None
        self.btSynFilename = None
        self.synFileName = None
        self.title("Synopsis Data Engine")
        self.existing_synopses = {}

        self.geometry("{0}x{0}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))

        # contains everything
        main_container = customtkinter.CTkFrame(self)
        main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        # buttons to select the frames
        self.seg_button = customtkinter.CTkSegmentedButton(main_container, command=self.frame_selector)
        self.seg_button.pack(side=tkinter.TOP, fill=tkinter.X, expand=False, padx=10, pady=10)
        #self.seg_button.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.seg_button.configure(
            values=["Dataset Management", "Create Synopsis", "Query Synopsis", "Query Spatial Synopsis"])
        # left side panel -> for frame selection
        left_side_panel = customtkinter.CTkFrame(main_container, width=100)
        self.set_left_side_panel(left_side_panel)

        # right side panel -> to show the frame1 or frame 2
        self.right_side_panel = customtkinter.CTkFrame(main_container)
        self.right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        self.right_side_container = customtkinter.CTkFrame(self.right_side_panel,fg_color="#000811")
        self.right_side_container.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=0, pady=0)

        App.frames['frame1'] = customtkinter.CTkFrame(main_container, fg_color="red")
        bt_from_frame1 = customtkinter.CTkButton(App.frames['frame1'], text="Test 1", command=lambda: print("test 1"))
        bt_from_frame1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        App.frames['frame2'] = customtkinter.CTkFrame(main_container)
        App.frames['frame3'] = customtkinter.CTkFrame(main_container)
        App.frames['frame4'] = customtkinter.CTkFrame(main_container)
        #bt_from_frame3 = customtkinter.CTkButton(App.frames['frame3'], text="Test 2", command=lambda: print("test 3"))
        #bt_from_frame3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        setFrame1(main_container)

        frame2 = CreateSynFrame(self)
        frame2.set_frame2()
        frame3 = QueryNormal(self)
        frame3.set_frame3()
        frame4 = QuerySpatial(self)
        frame4.set_frame4()

    def init_syn_file(self):
        # if file does not exist, create it
        # check if file exists, if not create it
        try:
            with open(self.btSynFilename.get(), "r") as file:
                pass
        except FileNotFoundError:
            with open(self.btSynFilename.get(), "w") as file:
                file.write("")


    def add_syn_to_file(self, request):

        if os.path.isfile(self.sde_parameters["filename"]):
            with open(self.sde_parameters["filename"], "a") as file:
                file.write(str(request) + "\n")
        else:
            with open(self.sde_parameters["filename"], "w") as file:
                file.write(str(request) + "\n")

    def read_syns_from_file(self):
        if os.path.isfile(self.sde_parameters["filename"]):
            with open(self.sde_parameters["filename"], "r") as file:
                for line in file:
                    request = Request.from_string(line)
                    self.existing_synopses[request["uid"]] = request


# StockID, price, Queryable, StockID;price;Queryable;0.002;0.99;4, 1, -50, 100, 0, 100, 16
# import tkinter
# import tkinter.messagebox
# import customtkinter
#
# customtkinter.set_appearance_mode("dark")
# customtkinter.set_default_color_theme("green")
#
# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()
#
#         # configure window
#         self.title("Synopsis Data Engine")
#         self.geometry(f"{1100}x{580}")
#
#         # configure grid layout (4x4)
#         self.grid_columnconfigure(1, weight=1)
#         self.grid_columnconfigure((2, 3), weight=0)
#         self.grid_rowconfigure((0, 1, 2), weight=1)
#
#         # create sidebar frame with widgets
#         self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
#         self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
#         self.sidebar_frame.grid_rowconfigure(4, weight=1)
#         self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter",
#                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
#         self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
#         self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
#         self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
#         self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
#         self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
#         self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
#         self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
#         self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
#         self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
#         self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
#                                                                        values=["Light", "Dark", "System"],
#                                                                        command=self.change_appearance_mode_event)
#         self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
#         self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
#         self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
#         self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
#                                                                values=["80%", "90%", "100%", "110%", "120%"],
#                                                                command=self.change_scaling_event)
#         self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
#
#         # create main entry and button
#         self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
#         self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
#
#         self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
#                                                      text_color=("gray10", "#DCE4EE"))
#         self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
#
#         # create textbox
#         self.textbox = customtkinter.CTkTextbox(self, width=250)
#         self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
#
#         # create tabview
#         self.tabview = customtkinter.CTkTabview(self, width=250)
#         self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
#         self.tabview.add("CTkTabview")
#         self.tabview.add("Tab 2")
#         self.tabview.add("Tab 3")
#         self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
#         self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)
#
#         self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
#                                                         values=["Value 1", "Value 2", "Value Long Long Long"])
#         self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
#         self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
#                                                     values=["Value 1", "Value 2", "Value Long....."])
#         self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
#         self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
#                                                            command=self.open_input_dialog_event)
#         self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
#         self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
#         self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)
#
#         # create radiobutton frame
#         self.radiobutton_frame = customtkinter.CTkFrame(self)
#         self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
#         self.radio_var = tkinter.IntVar(value=0)
#         self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
#         self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
#         self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var,
#                                                            value=0)
#         self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
#         self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var,
#                                                            value=1)
#         self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
#         self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var,
#                                                            value=2)
#         self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")
#
#         # create slider and progressbar frame
#         self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
#         self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
#         self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
#         self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
#         self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
#         self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
#         self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
#         self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
#         self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
#         self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
#         self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
#         self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
#         self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
#         self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
#         self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
#         self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")
#
#         # create scrollable frame
#         self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
#         self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
#         self.scrollable_frame.grid_columnconfigure(0, weight=1)
#         self.scrollable_frame_switches = []
#         for i in range(100):
#             switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
#             switch.grid(row=i, column=0, padx=10, pady=(0, 20))
#             self.scrollable_frame_switches.append(switch)
#
#         # create checkbox and switch frame
#         self.checkbox_slider_frame = customtkinter.CTkFrame(self)
#         self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
#         self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
#         self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
#         self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
#         self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
#         self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
#         self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")
#
#         # set default values
#         self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
#         self.checkbox_3.configure(state="disabled")
#         self.checkbox_1.select()
#         self.scrollable_frame_switches[0].select()
#         self.scrollable_frame_switches[4].select()
#         self.radio_button_3.configure(state="disabled")
#         self.appearance_mode_optionemenu.set("Dark")
#         self.scaling_optionemenu.set("100%")
#         self.optionmenu_1.set("CTkOptionmenu")
#         self.combobox_1.set("CTkComboBox")
#         self.slider_1.configure(command=self.progressbar_2.set)
#         self.slider_2.configure(command=self.progressbar_3.set)
#         self.progressbar_1.configure(mode="indeterminnate")
#         self.progressbar_1.start()
#         self.textbox.insert("0.0",
#                             "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
#         self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
#         self.seg_button_1.set("Value 2")
#
#     def open_input_dialog_event(self):
#         dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
#         print("CTkInputDialog:", dialog.get_input())
#
#     def change_appearance_mode_event(self, new_appearance_mode: str):
#         customtkinter.set_appearance_mode(new_appearance_mode)
#
#     def change_scaling_event(self, new_scaling: str):
#         new_scaling_float = int(new_scaling.replace("%", "")) / 100
#         customtkinter.set_widget_scaling(new_scaling_float)
#
#     def sidebar_button_event(self):
#         print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()