import json
import re

import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import Draw

from src.synMap import SynMap


def display_responses():
    st.subheader("📊 Query Results")

    if not st.session_state.responses:
        st.info("No results yet. Add one above.")
        return

    # Prepare data for table
    rows = []
    st.session_state.synMapClass = SynMap()
    c = 0
    for r in st.session_state.responses:
        syn = r["synopsis"]
        rows.append({"Query ID": c,
            "Estimation": r["response"]["estimation"],
            "Query Parameters": ", ".join(r["response"]["param"]),
            "Synopsis UID": syn["uid"],
            "Synopsis Type": st.session_state.synMapClass.getSynName(syn["synopsisID"])
        })
        c += 1

    df = pd.DataFrame(rows)

    # Sort or format if needed
    df = df.sort_values(by="Query ID", ascending=False)

    # --- Nice table display ---
    st.dataframe(df, use_container_width=True)



def load_synopses():
    dataset = st.session_state.current_dataset if st.session_state.current_dataset else st.warning(
        "No dataset selected.")

    st.session_state.existing_synopses = {}

    req = {
        "key": dataset["dataSetkey"],
        "streamID": dataset["StreamID"],
        "synopsisID": 1,
        "requestID": 777,
        "dataSetkey": dataset["dataSetkey"],
        "param": ["synopses"],
        "noOfP": st.session_state.sde_parameters["parallelization"],
        "uid": 5,
        # "externalUID": "getListOfsynopses"
    }

    resp = st.session_state.sde.send_request(req, "getListOfsynopses")

    if resp is None:
        st.error("Error loading synopses.")
        return
    synopses = extract_json_from_content(resp)

    for syn in synopses:
        st.session_state.existing_synopses[syn["externalUID"]] = syn

    st.session_state.ui_stage = "select_synopses_to_query"


def extract_json_from_content(data):
    if data:
        content = data['content']
        matches = re.findall(r'Syn_\d+_\{(.*?)\}', content, re.DOTALL)
        synopses = []

        for match in matches:
            json_str = '{' + match.strip().replace('\n', '').replace(' ', '') + '}'
            try:
                synopses.append(json.loads(json_str))
            except json.JSONDecodeError:
                print("Invalid JSON structure in 'content'.")

        return synopses


def query_synopses():
    st.header("Query Synopsis")
    if "ui_stage" not in st.session_state or st.session_state.ui_stage == "select_synopsis":

        # Ensure required session state
        if st.button("Load Existing Synopses"):
            load_synopses()
    if st.session_state.get("ui_stage") == "select_synopses_to_query":
        if "selected_synopsis_uid" not in st.session_state:
            st.session_state.selected_synopsis_uid = None

        # Step 1: Choose Existing Synopsis
        st.subheader("Step 1: Select Existing Synopsis")

        synopsis_labels = [
            f"{uid} | {syn['synopsisID']} | {syn['dataSetkey']}"
            for uid, syn in st.session_state.existing_synopses.items()
        ]
        selected_synopsis = st.selectbox(
            "Select a synopsis to query:",
            options=["-- Select a synopsis --"] + synopsis_labels,
            key="query_synopsis_selector")

        if selected_synopsis != "-- Select a synopsis --":
            if st.button("Confirm Synopsis Selection"):
                uid = selected_synopsis.split(" | ")[0]
                st.session_state.selected_synopsis_uid = uid
                if st.session_state.existing_synopses[uid]["synopsisID"] == 30:
                    st.session_state.ui_stage = "spatial_query_parameters"
                    st.session_state.basic_sketch_to_query = st.session_state.existing_synopses[uid]["param"][4]
                else:
                    st.session_state.ui_stage = "regular_query_parameters"
    if st.session_state.ui_stage == "spatial_query_parameters":
        show_spatial_query_form()
    if st.session_state.ui_stage == "regular_query_parameters":
        show_query_form()
    if st.session_state.ui_stage != "select_synopsis" and st.button("Reload Synopses"):
        load_synopses()
        st.rerun()


def extract_bounds(geojson):
    if not geojson or "geometry" not in geojson or not geojson["geometry"].get("coordinates"):
        return None

    try:
        coords = geojson["geometry"]["coordinates"][0]
        lats = [pt[1] for pt in coords]
        lons = [pt[0] for pt in coords]
        return {
            "minX": min(lons)*100,
            "maxX": max(lons)*100,
            "minY": min(lats)*100,
            "maxY": max(lats)*100
        }
    except (IndexError, KeyError, TypeError):
        st.error("Invalid GeoJSON format.")
        return None


def process_spatial_query_submission(uid):
    raw_param = st.session_state[f"spatial_query_params_{uid}"]
    if not raw_param.strip():
        st.error("Please provide query parameters.")
        return
    basic_param_list = [str(x.strip()) for x in raw_param.split(",")]
    region = st.session_state["spatial_filter_bounds"]
    basic_sketch_id = st.session_state.basic_sketch_to_query
    st.write("Basic Sketch ID:", basic_sketch_id)
    spatial_params = [f"{region[k]:.5f}" for k in ["minX", "maxX", "minY", "maxY"]] + [basic_sketch_id]

    param_list = spatial_params + basic_param_list
    request_data = build_query_request(uid, param_list)

    response = st.session_state.sde.send_request(request_data, "spatialQuery")

    if response:
        st.success("Query submitted successfully.")
        display_query_result(response, st.session_state.existing_synopses[uid])
    else:
        st.error("No response from server.")
    st.session_state.query_submitted = False


def show_spatial_query_form():
    st.subheader("Step 2: Spatial Query Parameters")

    uid = st.session_state.selected_synopsis_uid
    syn = st.session_state.existing_synopses[uid]
    dataset = st.session_state.current_dataset

    center_lat = (dataset["minY"]/100 + dataset["maxY"]/100) / 2
    center_lon = (dataset["minX"]/100 + dataset["maxX"]/100) / 2

    m = folium.Map(location=[center_lat, center_lon], zoom_start=7)
    folium.Rectangle(
        bounds=[[dataset["minY"]/100, dataset["minX"]/100], [dataset["maxY"]/100, dataset["maxX"]/100]],
        color="blue", fill=True, fill_opacity=0.1, tooltip="Dataset Bounds"
    ).add_to(m)

    if "spatial_filter_bounds" in st.session_state:
        b = st.session_state["spatial_filter_bounds"]
        folium.Rectangle(
            bounds=[[b["minY"]/100, b["minX"]/100], [b["maxY"]/100, b["maxX"]/100]],
            color="red", fill=True, fill_opacity=0.3, tooltip="Selected Region"
        ).add_to(m)

    Draw(export=True).add_to(m)
    map_data = st_folium(m, height=500, width=700)

    if map_data and "last_active_drawing" in map_data:
        region_bounds = extract_bounds(map_data["last_active_drawing"])
        if region_bounds and region_bounds != st.session_state.get("spatial_filter_bounds"):
            st.session_state["spatial_filter_bounds"] = region_bounds

            st.session_state["region_selected"] = True
            st.success("Region selected!")
            st.rerun()
            # Show query input form

    if st.session_state.get("region_selected", False):
        with st.form(key=f"spatial_query_form_{uid}"):
            st.session_state[f"spatial_query_params_{uid}"] = st.text_area(
                "Enter spatial query parameters (comma-separated):",
                value=st.session_state.get(f"spatial_query_params_{uid}", ""),
                key=f"spatial_query_input_{uid}"
            )
            if "spatial_filter_bounds" not in st.session_state:
                st.error("Please select a region before submitting the query.")
            else:
                if st.form_submit_button("Query Synopsis"):
                    st.write("Spatial query submitted")
                    st.session_state.query_submitted = True
                    process_spatial_query_submission(uid)
                    st.rerun()


def show_query_form():
    """Main UI block for regular_query_parameters stage."""
    st.subheader("Step 2: Query Parameters")
    uid = st.session_state.selected_synopsis_uid
    ensure_query_state(uid)

    with st.form(key=f"query_form_{uid}"):
        st.session_state[f"query_params_{uid}"] = st.text_area(
            "Enter query parameters (comma-separated):",
            value=st.session_state[f"query_params_{uid}"],
            key=f"query_input_{uid}"
        )
        if st.form_submit_button("Query Synopsis"):
            st.session_state.query_submitted = True
            process_query_submission(uid)
            st.rerun()


def display_query_result(response, syn):
    res = {"response": response,
           "synopsis": syn}

    st.session_state.responses.append(res)


def ensure_query_state(uid):
    """Initialize session state for query parameters if not already present."""
    st.session_state.setdefault(f"query_params_{uid}", "")
    st.session_state.setdefault(f"query_input_{uid}", "")


def render_synopsis_details(uid):
    """Display selected synopsis metadata."""
    syn = st.session_state.existing_synopses[uid]
    st.write(f"Selected Synopsis: {syn['synopsisID']}")
    st.write(f"Dataset Key: {syn['dataSetkey']}")
    st.write(f"Stream ID: {syn['streamID']}")
    st.write(f"No of P: {syn['noOfP']}")


def build_query_request(uid, param_list):
    """Construct the query request payload."""
    syn = st.session_state.existing_synopses[uid]
    return {
        "key": syn["dataSetkey"],
        "streamID": syn["streamID"],
        "synopsisID": syn["synopsisID"],
        "requestID": 3,
        "dataSetkey": syn["dataSetkey"],
        "param": param_list,
        "noOfP": syn["noOfP"],
        "uid": syn["uid"],
        # "externalUID": f"Estimate:{syn['uid']}"
    }


def process_query_submission(uid):
    """Handle query submission logic."""
    raw_param = st.session_state[f"query_params_{uid}"]
    if not raw_param.strip():
        st.error("Please provide query parameters.")
        return

    param_list = [x.strip() for x in raw_param.split(",")]
    request_data = build_query_request(uid, param_list)

    response = st.session_state.sde.send_request(request_data, "submitQuery")

    if response:
        st.success("Query submitted successfully.")
        display_query_result(response, st.session_state.existing_synopses[uid])
    else:
        st.error("No response from server.")
    st.session_state.query_submitted = False
