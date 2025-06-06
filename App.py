import ast
import re
from sde_py_lib.client import Client
from stelar.client import Client as stelarClient
from MinIOClient import MinIOClient

import streamlit as st
import json


class App:
    def __init__(self, local):
        # Credentials are always loaded from the URI since the Tokens required 
        # for the STELAR client are passed as query parameters and are prone to expire.
        if local:
            st.session_state.credentials = self.load_credentials("./credentials_local.json")
        else:
            st.session_state.credentials = self.load_credentials_from_uri()

        st.write("DEBUG: Loaded credentials:", st.session_state.credentials)
        bootstrap_servers = st.session_state.credentials["kafka"]["bootstrap_servers"]
        if bootstrap_servers:
            st.session_state.sde_parameters = {
                "data_topic": "data",
                "request_topic": "request",
                "output_topic": "estimation",
                "logging_topic": "logging",
                "bootstrap_servers": bootstrap_servers,
                "parallelization": "2",
                "syn_filename": "synopses.txt",
                "dataset_filename": "datasets.txt",
            }
        if "sde" not in st.session_state:
            st.session_state.sde = Client(
                st.session_state.sde_parameters["bootstrap_servers"],
                message_queue_size=20,
                response_timeout=20,
            )

        new_token_json = st.session_state.credentials["token_json"]

        # Check if the client exists and the token has changed or expired
        if "stelar_client" in st.session_state and "token" in st.session_state:
            if st.session_state.token != new_token_json:  # Assuming the client has a `token_json` attribute
                st.session_state.stelar_client = None  # Clear the old client

        # Initialize the client with the new token_json
        if "stelar_client" not in st.session_state or st.session_state.stelar_client is None:
            st.session_state.token = new_token_json
            st.session_state.stelar_client = stelarClient(
                base_url=st.session_state.credentials["stelar_client"]["url"],
                token_json=new_token_json,
            )

        new_minio_credentials = st.session_state.credentials["minio"]
        if "minio_client" in st.session_state:
            if st.session_state.minio_client.credentials != new_minio_credentials:
                st.session_state.minio_client = None

        if "minio_client" not in st.session_state or st.session_state.minio_client is None:
            st.session_state.minio_client = MinIOClient(
                bucket_name=st.session_state.credentials["minio"]["bucket"],
                credentials=st.session_state.credentials,
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
        with open(file_path, "r") as file:
            return json.load(file)

    @staticmethod
    @st.cache_data
    def load_credentials_from_uri():
        """
        Load credentials from a URI.
        The URI should contain query parameters for the credentials.
        """
        qparams = st.query_params
        creds = {
            "stelar_client": {
                "url": qparams.get("api", "https://klms.stelar.gr/stelar"),
                "access_token": qparams.get("access_token", ""),
                "refresh_token": qparams.get("refresh_token", ""),
                "expires_in": int(qparams.get("expires_in", "0")),
                "refresh_expires_in": int(qparams.get("refresh_expires_in", "0")),
                "username": qparams.get("username", ""),
            },
            "token_json": {
                "access_token": qparams.get("access_token", ""),
                "refresh_token": qparams.get("refresh_token", ""),
                "expires_in": int(qparams.get("expires_in", "0")),
                "refresh_expires_in": int(qparams.get("refresh_expires_in", "0")),
            },
            "minio": {
                "endpoint": qparams.get("s3_endpoint", ""),
                "access_key": qparams.get("access_key", ""),
                "secret_key": qparams.get("secret_key", ""),
                "session_token": qparams.get("session_token", ""),
                "bucket": qparams.get("bucket", "klms-bucket"),
            },
            "kafka": {
                "bootstrap_servers": qparams.get(
                    "kafka_bootstrap_servers", "sde.petrounetwork.gr:19092"
                ),
            },
        }
        return creds

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
        st.write("Try to load datasets from txt_files/datasets.txt")

        with open("./txt_files/datasets.txt", "r") as file:
            datasets = file.readlines()
            st.session_state.existing_datasets = {}
            for d in datasets:
                dataset = ast.literal_eval(d)
                st.write("DEBUG: Loading dataset:", dataset["dataSetkey"])
                st.session_state.existing_datasets[dataset["dataSetkey"]] = dataset
        return
