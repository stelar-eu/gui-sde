import json
import re

import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import Draw


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
        "externalUID": "getListOfsynopses"
    }

    resp = st.session_state.sde.send_request(req, "getListOfsynopses")

    if resp is None:
        st.error("Error loading synopses.")
        return

    st.write("Response:", resp)  # or use st.json(resp) for better formatting

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
    if "ui_stage" not in st.session_state or st.session_state.ui_stage == "done" or st.session_state.ui_stage == "select_synopsis":

        # Ensure required session state
        if st.button("Load Existing Synopses"):
            # st.session_state.existing_synopses = {"syn_1": {
            #     "synopsisID": 30,
            #     "dataSetkey": "synopses_experiment",
            #     "streamID": "S1",
            #     "noOfP": 2,
            #     "uid": 5,
            #     "param": ["key1", "key2"],
            #     "externalUID": "syn_1"
            # }}
            # example synopsis
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
        selected_label = st.selectbox("Select a synopsis to query:", options=synopsis_labels,
                                      key="query_synopsis_selector")

        if selected_label:
            uid = selected_label.split(" | ")[0]
            st.session_state.selected_synopsis_uid = uid
            if st.session_state.existing_synopses[uid]["synopsisID"] == 30:
                st.session_state.ui_stage = "spatial_query_parameters"
            else:
                st.session_state.ui_stage = "regular_query_parameters"
    if st.session_state.ui_stage == "spatial_query_parameters":
        show_spatial_query_form()
    if st.session_state.ui_stage == "regular_query_parameters":
        show_query_form()
    else:
        st.error("Invalid UI stage. Please reload the app.")


def extract_bounds(geojson):
    coords = geojson["geometry"]["coordinates"][0]
    lats = [pt[1] for pt in coords]
    lons = [pt[0] for pt in coords]
    return {
        "minX": min(lons),
        "maxX": max(lons),
        "minY": min(lats),
        "maxY": max(lats)
    }


def show_spatial_query_form():
    st.subheader("Step 2: Spatial Query Parameters")

    uid = st.session_state.selected_synopsis_uid
    syn = st.session_state.existing_synopses[uid]
    dataset = st.session_state.current_dataset

    center_lat = (dataset["minY"] + dataset["maxY"]) / 2
    center_lon = (dataset["minX"] + dataset["maxX"]) / 2

    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)
    folium.Rectangle(
        bounds=[[dataset["minY"], dataset["minX"]], [dataset["maxY"], dataset["maxX"]]],
        color="blue", fill=True, fill_opacity=0.1, tooltip="Dataset Bounds"
    ).add_to(m)

    Draw(export=True).add_to(m)
    map_data = st_folium(m, height=500, width=700)

    if map_data and "last_active_drawing" in map_data:
        region_bounds = extract_bounds(map_data["last_active_drawing"])
        st.session_state["spatial_filter_bounds"] = region_bounds
        st.success("Region selected!")

        # Show query input form
        st.write("Selected region bounds:", region_bounds)
        with st.form(key=f"spatial_query_form_{uid}"):
            raw_param = st.text_area(
                "Enter additional query parameters (comma-separated):",
                key=f"spatial_query_input_{uid}"
            )

            if st.form_submit_button("Query Synopsis"):
                if not raw_param.strip():
                    st.error("Please provide query parameters.")
                    return

                param_list = [x.strip() for x in raw_param.split(",")]

                # Add spatial filtering parameters
                region = st.session_state["spatial_filter_bounds"]
                spatial_params = [
                    f"minX={region['minX']}",
                    f"maxX={region['maxX']}",
                    f"minY={region['minY']}",
                    f"maxY={region['maxY']}"
                ]

                request_data = {
                    "key": syn["dataSetkey"],
                    "streamID": syn["streamID"],
                    "synopsisID": syn["synopsisID"],
                    "requestID": 4,
                    "dataSetkey": syn["dataSetkey"],
                    "param": spatial_params + param_list,
                    "noOfP": syn["noOfP"],
                    "uid": syn["uid"],
                    "externalUID": f"SpatialEstimate:{syn['uid']}"
                }

                response = st.session_state.sde.send_request(request_data, request_data["externalUID"])
                # response = {"content": "Spatial Estimate: 98765", "status": "success"}  # Mock

                if response:
                    st.success("Spatial query submitted successfully.")
                    display_query_result(response, syn)
                    st.session_state.ui_stage = "done"
                else:
                    st.error("No response from server.")


def show_query_form():
    """Main UI block for regular_query_parameters stage."""
    st.subheader("Step 2: Query Parameters")
    uid = st.session_state.selected_synopsis_uid
    ensure_query_state(uid)

    with st.form(key=f"query_form_{uid}"):
        render_synopsis_details(uid)
        st.session_state[f"query_params_{uid}"] = st.text_area(
            "Enter query parameters (comma-separated):",
            value=st.session_state[f"query_params_{uid}"],
            key=f"query_input_{uid}"
        )
        if st.form_submit_button("Query Synopsis"):
            st.write("Query submitted")
            st.session_state.query_submitted = True
            process_query_submission(uid)


def display_query_result(response, syn):
    st.subheader("Query Result")

    st.markdown("### 🧮 Estimate Output")
    result_data = {
        "Estimate": response,
        "UID": syn["uid"],
        "Synopsis Type": syn["synopsisID"],
        "Dataset": syn["dataSetkey"],
        "Stream ID": syn["streamID"],
        "No of P": syn["noOfP"],
        "Parameters": ", ".join(syn["param"]) if isinstance(syn["param"], list) else str(syn["param"])
    }

    for key, val in result_data.items():
        st.write(f"**{key}:** {val}")


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
        "externalUID": f"Estimate:{syn['uid']}"
    }


def process_query_submission(uid):
    """Handle query submission logic."""
    raw_param = st.session_state[f"query_params_{uid}"]
    if not raw_param.strip():
        st.error("Please provide query parameters.")
        return

    param_list = [x.strip() for x in raw_param.split(",")]
    request_data = build_query_request(uid, param_list)

    # Simulated response – replace with actual call:

    response = st.session_state.sde.send_request(request_data, request_data["externalUID"])

    if response:
        st.success("Query submitted successfully.")
        display_query_result(response, st.session_state.existing_synopses[uid])
    else:
        st.error("No response from server.")
    st.session_state.query_submitted = False
    st.session_state.ui_stage = "done"
