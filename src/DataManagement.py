import streamlit as st


def dataset_management():
    st.header("Dataset Management")

    # Load Datasets Button
    if st.button("Load Datasets"):
        load_datasets()


def load_datasets():
    shown_datasets = []
    for txt_name in st.session_state.existing_datasets:
        ds = st.session_state.stelar_client.datasets[txt_name]
        shown_datasets.append(ds)

    if shown_datasets:
        # Display datasets in a radio button list
        selected_dataset_name = st.radio(
            "Select Dataset",
            options=[dataset.name for dataset in shown_datasets],
            key="dataset_selection"
        )

        # Handle Dataset Selection
        if selected_dataset_name:
            if selected_dataset_name in st.session_state.existing_datasets:
                st.session_state.current_dataset = st.session_state.existing_datasets[selected_dataset_name]
                st.session_state.selected_dataset = st.session_state.stelar_client.datasets[selected_dataset_name]
                st.success(f"Selected Dataset: {selected_dataset_name}")
            else:
                st.error(f"Dataset {selected_dataset_name} not found in existing datasets")
    else:
        st.warning("No datasets available to display.")
