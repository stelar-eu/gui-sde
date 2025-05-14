import os

import streamlit as st

def get_sidebar():
    """
    Create a sidebar for the Streamlit app to manage SDE parameters.
    """
    st.sidebar.title("SDE Parameters")

    # Initialize SDE parameters
    st.session_state.sde_parameters = {
        "data_topic": "default_topic",
        "bootstrap_servers": "localhost:9092",
        "parallelization": 1,
        "synopsis_spec": None,
        "synopsis": None,
        "dataset_key": None,
        "stream_id": None
    }

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
            st.session_state.credentials["klms"]["access_key"],
            st.session_state.credentials["klms"]["secret_key"],
            st.session_state.credentials["klms"]["session_token"],
            st.session_state.credentials["klms"]["endpoint"]
        )
        if response:
            st.sidebar.success("Connected to running SDE")
        else:
            st.sidebar.error("Error connecting to SDE")
    st.sidebar.image("./test_images/Logo - Stelar project.jpg")