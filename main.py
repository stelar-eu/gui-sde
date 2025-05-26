

import streamlit as st

from DataManagement import dataset_management
from App import App
from create_synopsis import create_synopsis
from query_synopses import query_synopses
from sidebar import get_sidebar

from urllib.parse import urlparse

# Initialize Streamlit app
st.set_page_config(page_title="STELAR Synopsis Data Engine", layout="wide")

def parse_s3_url(s3_url):
    """
    Parse the S3 URL to extract the bucket name and object path.
    """
    parsed_url = urlparse(s3_url)
    bucket_name = parsed_url.netloc  # Extracts 'klms-bucket'
    object_path = parsed_url.path.lstrip('/')  # Extracts 'profile.txt'
    return bucket_name, object_path


if "parse_s3_url" not in st.session_state:
    st.session_state.parse_s3_url = parse_s3_url

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
