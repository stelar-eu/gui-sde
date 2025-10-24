import ast
import atexit
import os

from sde_py_lib.client import Client
from stelar.client import Client as stelarClient
from MinIOClient import MinIOClient

import streamlit as st
from urllib.parse import urlparse, parse_qs


def get_creds(qparams: dict):
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
            "bucket": qparams.get("bucket", "sde-bucket"),
        },
        "kafka": {
            "bootstrap_servers": qparams.get("kafka_bootstrap_servers", "sde.stelar.gr:29092,sde.stelar.gr:19092"),
        },
    }
    return creds


def read_metainfo_existing_datasets():
    # Here, we read the datasets.txt file.
    # The file should contain a list of dictionaries, each representing a dataset.
    # Each dictionary should contain the following keys:
    # - dataSetkey
    # - DatasetName
    # - StreamID
    # - Attribute list
    # Get absolute path to txt_files from project root
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "txt_files", "datasets.txt")

    with open(file_path, "r") as file:
        datasets = file.readlines()
        st.session_state.existing_datasets = {}
        for d in datasets:
            dataset = ast.literal_eval(d)
            st.session_state.existing_datasets[dataset["dataSetkey"]] = dataset
    return


class App:
    def __init__(self, local=False):
        # Register the cleanup function to close the Kafka consumer and producer
        atexit.register(self.cleanup)
        query_params = st.query_params.to_dict()

        # Credentials are always loaded from the URI since the Tokens required 
        # for the STELAR client are passed as query parameters and are prone to expire.
        if local:
            url = open("./txt_files/local_url.txt", "r").read()
            creds = self.load_credentials_from_url_local(url)
        else:
            creds = self.load_credentials_from_uri(query_params)
        creds_changed = ("credentials" not in st.session_state or st.session_state.credentials != creds)

        if creds_changed:
            st.session_state.credentials = creds
            st.session_state.token = creds["token_json"]
            st.session_state.stelar_client = None  # Force re-initialization of the client


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

        if "sde" in st.session_state:
            self.cleanup()
            st.session_state.sde = None
            # del st.session_state.sde

        if "sde" not in st.session_state or st.session_state.sde is None:
            st.session_state.sde = Client(
                str(st.session_state.sde_parameters["bootstrap_servers"]),
                st.session_state.sde_parameters['request_topic'],
                st.session_state.sde_parameters['data_topic'],
                st.session_state.sde_parameters['output_topic'],
                st.session_state.sde_parameters['logging_topic'],
                message_queue_size=20,
                response_timeout=20,
                parallelism=int(st.session_state.sde_parameters['parallelization'])
            )

        if st.session_state.stelar_client is None:
            creds = st.session_state.credentials
            st.session_state.stelar_client = stelarClient(
                base_url=creds["stelar_client"]["url"],
                username=creds["stelar_client"]["username"],
                token_json=creds["token_json"],
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
            read_metainfo_existing_datasets()
        if "existing_synopses" not in st.session_state:
            st.session_state.existing_synopses = {}
        if "current_dataset" not in st.session_state:
            st.session_state.current_dataset = None
        if "responses" not in st.session_state:
            st.session_state.responses = []

    @staticmethod
    @st.cache_data
    def load_credentials_from_url_local(url: str):
        """
        Parse a full URL and return credentials in the same structure as load_credentials_from_uri().
        """
        parsed_url = urlparse(url)
        qparams = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}  # flatten single values

        return get_creds(qparams)

    @staticmethod
    @st.cache_data
    def load_credentials_from_uri(query_params: dict):
        """
        Load credentials from a URI.
        The URI should contain query parameters for the credentials.
        """
        return get_creds(query_params)

    def cleanup(self):
        """Gracefully shuts down the Kafka consumer and producer."""
        if "sde" in st.session_state:
            try:
                st.session_state.sde.close()
                print("Kafka consumer and producer closed successfully.")
            except Exception as e:
                print(f"Error during Kafka cleanup: {e}")