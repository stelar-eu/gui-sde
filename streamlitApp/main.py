

import streamlit as st
import json
from datetime import datetime
from DataClient import DataClient
from datasetMap import DatasetMap

from sde_py_lib.model import Synopsis, SynopsisSpec
from DataManagement import dataset_management
from streamlitApp.App import App
from streamlitApp.create_synopsis import create_synopsis
from streamlitApp.query_synopses import query_synopses
from streamlitApp.sidebar import get_sidebar

# Initialize Streamlit app
st.set_page_config(page_title="STELAR Synopsis Data Engine", layout="wide")
st.title("STELAR Synopsis Data Engine")

# Create App instance
App()

# Sidebar for SDE Parameters
get_sidebar()

# Dataset Management
dataset_management()

# Create Synopsis
create_synopsis()

# Query Synopsis
query_synopses()
