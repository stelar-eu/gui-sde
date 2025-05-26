import ast
import re
from sde_py_lib.client import Client
from stelar.client import Client as stelarClient
from MinIOClient import MinIOClient

import streamlit as st
import json


class App:
    def __init__(self):
        if "credentials" not in st.session_state:
            st.text_input("Enter your credentials file path:",
                          key="credentials_path", value="./streamlitApp/credentials_local.json")
            # st.session_state.credentials = self.load_credentials('./streamlitApp/credentials.json')

            st.session_state.credentials = self.load_credentials(st.session_state.credentials_path)

        if "sde_parameters" not in st.session_state:
            st.session_state.sde_parameters = {
                "data_topic": "data",
                "request_topic": "request",
                "output_topic": "estimation",
                "logging_topic": "logging",
                "bootstrap_servers": st.session_state.credentials["kafka"]["bootstrap_servers"],
                "parallelization": "2",
                "syn_filename": "synopses.txt",
                "dataset_filename": "datasets.txt"
            }
        if "sde" not in st.session_state:
            st.session_state.sde = Client(st.session_state.sde_parameters["bootstrap_servers"],
                                      message_queue_size=20, response_timeout=20)
        if "stelar_client" not in st.session_state:
            st.session_state.stelar_client = stelarClient(
                base_url=st.session_state.credentials['stelar_client']['url'],
                username=st.session_state.credentials['stelar_client']['username'],
                password=st.session_state.credentials['stelar_client']['password']
            )
        if "minio_client" not in st.session_state:
            st.session_state.minio_client = MinIOClient(
                bucket_name="klms-bucket",
                credentials=st.session_state.credentials
            )

        if "existing_datasets" not in st.session_state:
            st.session_state.existing_datasets = {}
        self.read_metainfo_existing_datasets()
        if "existing_synopses" not in st.session_state:
            st.session_state.existing_synopses = {}
        if "current_dataset" not in st.session_state:
            st.session_state.current_dataset = None

    @staticmethod
    @st.cache_data
    def load_credentials(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    @st.cache_data
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
            st.session_state.existing_datasets = {}
            for d in datasets:
                dataset = ast.literal_eval(d)

                st.session_state.existing_datasets[dataset["dataSetkey"]] = dataset
        return
