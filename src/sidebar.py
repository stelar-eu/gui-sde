from datetime import datetime
import streamlit as st
from src.DataClientStreamLit import DataClientStreamLit


def get_sidebar():
    """
    Create a sidebar for the Streamlit app to manage SDE parameters.
    """
    st.sidebar.title("SDE Parameters")

    if "sde_parameters" not in st.session_state:
        st.error("SDE parameters not initialized. Please check your connection to the SDE.")

    st.session_state.sde_parameters["data_topic"] = st.sidebar.text_input(
        "Data Topic",
        value=st.session_state.sde_parameters["data_topic"])
    st.session_state.sde_parameters["bootstrap_servers"] = st.sidebar.text_input(
        "Bootstrap Servers", value=st.session_state.sde_parameters["bootstrap_servers"]
    )
    st.session_state.sde_parameters["parallelization"] = st.sidebar.text_input(
        "Parallelization", value=st.session_state.sde_parameters["parallelization"]
    )

    if st.sidebar.button("Connect to SDE"):
        response = st.session_state.sde.send_storage_auth_request(
            st.session_state.credentials["minio"]["access_key"],
            st.session_state.credentials["minio"]["secret_key"],
            st.session_state.credentials["minio"]["session_token"],
            st.session_state.credentials["minio"]["endpoint"]
        )
        if response:
            st.sidebar.success("Connected to running SDE")
        else:
            st.sidebar.error("Error connecting to SDE")
    if st.sidebar.button("Send Data"):
        if st.session_state.current_dataset:
            resources = st.session_state.selected_dataset.resources
            for res in resources:
                if res.format != "Synopsis":
                    get_data_from_url(
                        res, st.session_state.current_dataset['dataSetkey'],
                        st.session_state.current_dataset['StreamID'])
            st.sidebar.success("All data has been sent to the Kafka topic")
        else:
            st.sidebar.error("No dataset selected")


def get_data_from_url(res, dataSetkey, StreamID):
    bucket_name, object_path = st.session_state.parse_s3_url(res.url)
    data = st.session_state.minio_client.get_object(bucket_name, object_path)
    start_time = datetime.now()
    rr = DataClientStreamLit(data, dataSetkey, res)
    rr.send(dataSetkey, StreamID)
    end_time = datetime.now()
    print("Time taken to send data to Kafka: ", end_time - start_time)
