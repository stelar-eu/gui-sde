import streamlit as st
from synMap import SynMap
from datetime import datetime


def create_synopsis():
    st.header("Create Synopsis")

    # Initialize synMap and basicSketchMap in session state
    if "ui_stage" not in st.session_state:
        st.session_state.ui_stage = "select_synopsis"
    if "synMap" not in st.session_state:
        st.session_state.synMap = SynMap.getSynMap(SynMap())
    if "basicSketchMap" not in st.session_state:
        st.session_state.basicSketchMap = SynMap.getBasicSketches(SynMap())
    if "u_name" not in st.session_state:
        st.session_state.u_name = ""
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

    # Dataset and StreamID
    if st.session_state.current_dataset is None:
        dataset_key = st.text_input("Dataset Key", key="dataset_key")
        stream_id = st.text_input("Stream ID", key="stream_id")
    else:
        dataset_key = st.session_state.current_dataset["dataSetkey"]
        stream_id = st.session_state.current_dataset["StreamID"]

    # Unique Name
    st.session_state.u_name = st.text_input("Unique Name", key="unique_name")

    # Synopsis Type Dropdown
    synopsis_type = st.selectbox(
        "Query Type - Synopsis Name",
        options=list(st.session_state.synMap.keys()),
        key="select_synopsis_type",
    )

    if st.button("Select"):
        if not dataset_key or not stream_id or not st.session_state.u_name:
            st.error("Please fill in all fields.")
            return

        if st.session_state.u_name in st.session_state.existing_synopses:
            st.error(f"Unique Name {st.session_state.u_name} already exists.")
            return

        st.session_state.synopsis_type = synopsis_type  # Save for later
        if synopsis_type == "Spatial Queries - SpatialSketch":
            st.session_state.ui_stage = "choose_basic_sketch"
        else:
            st.session_state.ui_stage = "custom_parameters"

    # Display the appropriate UI based on the selected stage
    if st.session_state.ui_stage == "choose_basic_sketch":
        choose_basic_sketch()
    if st.session_state.ui_stage == "spatial_sketch_parameters":
        spatial_sketch_parameters(st.session_state.basic_sketch_name)
    elif st.session_state.ui_stage == "custom_parameters":
        custom_parameters(st.session_state.synMap[st.session_state.synopsis_type])
    if st.session_state.ui_stage == "done":
        st.success("Synopsis successfully created!")

    # # Create Synopsis Button
    # if st.button("Select"):
    #     if not dataset_key or not stream_id or not st.session_state.u_name:
    #         st.error("Please fill in all fields.")
    #         return
    #
    #     if st.session_state.u_name in st.session_state.existing_synopses:
    #         st.error(f"Unique Name {st.session_state.u_name} already exists.")
    #         return
    #
    #     if synopsis_type == "Spatial Queries - SpatialSketch":
    #         choose_basic_sketch()
    #     else:
    #         custom_parameters(st.session_state.synMap[synopsis_type], st.session_state.current_dataset)


def choose_basic_sketch():
    st.subheader("Choose Basic Sketch")

    # Basic Sketch Dropdown
    basic_sketch_name = st.selectbox(
        "Basic Sketch Synopsis ID",
        options=list(st.session_state.basicSketchMap.keys()),
        key="select_basic_sketch_name",
    )

    # Select Basic Sketch Button
    if st.button("Select Basic Sketch"):
        if basic_sketch_name not in st.session_state.synMap:
            st.error("Invalid Basic Sketch.")
            return
        st.session_state.basic_sketch_name = basic_sketch_name
        st.session_state.ui_stage = "spatial_sketch_parameters"


def spatial_sketch_parameters(basic_sketch_name):
    st.subheader("Spatial Sketch Parameters")
    dataset = st.session_state.current_dataset

    syn = st.session_state.synMap["Spatial Queries - SpatialSketch"]
    basic_syn = st.session_state.synMap[basic_sketch_name]

    st.subheader(f"Parameters for {syn['name']}")

    basic_parameters = ["keyField", "valueField", "operationMode", "BasicSketchParameters", "BasicSketchSynID"]
    if "param_dict" not in st.session_state:
        st.session_state.param_dict = {}
        for param in syn["parameters"]:
            if param not in basic_parameters:
                st.session_state.param_dict[f"spatial_{param}"] = ""
            else:
                st.session_state.param_dict[f"basic_{param}"] = ""

    # Create a form for parameter inputs
    with st.form(key="spatial_parameters_form"):
        for param in syn["parameters"]:
            if param not in basic_parameters:
                st.session_state.param_dict[f"spatial_{param}"] = st.text_input(param, key=f"spatial_{param}")
        st.subheader(f"Parameters for Basic Sketch: {basic_syn['name']}")
        for param in basic_syn["parameters"]:
            if param in ["keyField", "valueField"] and dataset:
                st.session_state.param_dict[f"basic_{param}"] = st.selectbox(param, options=dataset["parameters"],
                                                                             key=f"basic_{param}")
            else:
                st.session_state.param_dict[f"basic_{param}"] = st.text_input(param, key=f"basic_{param}")
        # Submit button for the form
        if st.form_submit_button("Create Synopsis"):
            st.write("Form submitted")
            st.session_state.form_submitted = True
            syn_parameters = [st.session_state.param_dict[f"spatial_{param}"] for param in
                              st.session_state.synMap["Spatial Queries - SpatialSketch"]["parameters"]
                              if param not in basic_parameters]
            # basic_parameters as string with semicolon separator
            basic_parameters = [f"{st.session_state.param_dict[f'basic_{param}']}" for param in
                                st.session_state.synMap[basic_sketch_name]["parameters"]]
            # Combine parameters
            syn_parameters = combine_parameters(syn_parameters, basic_parameters)

            send_request(syn_parameters, basic_sketch_name)
            st.session_state.form_submitted = False

            st.session_state.ui_stage = "done"


def custom_parameters(syn):
    dataset = st.session_state.current_dataset
    st.write("dataset:", dataset)
    st.subheader(f"Parameters for {syn['name']}")
    if "param_dict" not in st.session_state:
        st.session_state.param_dict = {f"custom_{param}": "" for param in syn["parameters"]}
    # Create a form for parameter inputs
    with st.form(key="custom_parameters_form"):
        for param in syn["parameters"]:
            if dataset and param in dataset:
                # Dropdown for parameters in the dataset
                if param not in st.session_state.param_dict:
                    st.session_state.param_dict[f"custom_{param}"] = st.selectbox(
                        param,
                        options=dataset["parameters"],
                        index=dataset["parameters"].index(st.session_state.param_dict[f"custom_{param}"])
                        if st.session_state.param_dict[f"custom_{param}"] in dataset["parameters"] else 0,
                        key=f"custom_{param}",
                    )
            else:
                # Text input for other parameters
                st.session_state.param_dict[f"custom_{param}"] = st.text_input(
                    param,
                    value=st.session_state.param_dict[f"custom_{param}"],
                    key=f"custom_{param}",
                )

        # Submit button for the form
        if st.form_submit_button("Create Synopsis"):
            st.session_state.form_submitted = True
            syn_parameters = [str(st.session_state.param_dict[f"custom_{param}"]) for param in
                                        st.session_state.synMap[st.session_state.synopsis_type]["parameters"]]
            send_request(syn_parameters)
            st.session_state.form_submitted = False
            st.session_state.ui_stage = "done"


def combine_parameters(syn_parameters, basic_parameters):
    """
    Combines syn_parameters and basic_parameters into a single string
    delimited by ", " in the correct order.

    Args:
        syn_parameters (list): List of synopsis parameters.
        basic_parameters (list): List of basic parameters.

    Returns:
        str: Combined parameters as a single string.
    """
    # Combine the parameters in the correct order
    combined_parameters = [
        basic_parameters[0],  # Example: keyField
        basic_parameters[1],  # Example: valueField
        basic_parameters[2],  # Example: operationMode
        ";".join([str(param) for param in basic_parameters]),  # Basic parameters as a semicolon-separated string
        st.session_state.basicSketchMap[st.session_state.basic_sketch_name]["synID"],  # Basic Sketch Syn ID
        syn_parameters[0],  # Example: minX
        syn_parameters[1],  # Example: maxX
        syn_parameters[2],  # Example: minY
        syn_parameters[3],  # Example: maxY
        syn_parameters[4]  # Example: resolution
    ]
    # Join the combined parameters with ", " as the delimiter
    return ", ".join([str(param) for param in combined_parameters])


def send_request(syn_parameters, basic_sketch_name=None):
    st.write("Sending request to SDE...")
    # Collect parameters

    st.write("dataset right now:", st.session_state.current_dataset)

    # Prepare request data
    request_data = {
        "key": st.session_state.current_dataset["dataSetkey"],
        "streamID": st.session_state.current_dataset["StreamID"],
        "synopsisID": st.session_state.synMap[st.session_state.synopsis_type]["synID"],
        "requestID": 1,
        "dataSetkey": st.session_state.current_dataset["dataSetkey"],
        "param": syn_parameters,
        "noOfP": st.session_state.sde_parameters["parallelization"],
        "uid": st.session_state.u_name,
        "externalUID": f"create:{st.session_state.u_name}",
    }

    # Send request
    response = st.session_state.sde.send_request(request_data, f"create:{st.session_state.u_name}")
    if response:
        st.success(f"Synopsis Created: {response}")
        st.session_state.existing_synopses[st.session_state.u_name] = request_data
    else:
        st.error("No response from server.")
