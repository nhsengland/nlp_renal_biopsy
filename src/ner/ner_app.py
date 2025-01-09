# streamlit run ner_app.py -- --d "example_output/example_pipeline_17_06_24/llm.json"
# streamlit run ner_app.py -- --d "example_output/rb.json"
# streamlit run ner_app.py -- --d "example_output/data/ner_output_report_first100.json" 
# this is based off will poulett's code

from streamlit_annotation_tools import text_labeler
import streamlit as st
import argparse
import json
from src.extraction.extraction import Extraction
from src.config.experimental_config import load_experimental_config
from src.config.global_config import load_global_config
import os

# Predefined NER labels
PREDEFINED_LABELS = [
    "cortex_present",
    "medulla_present",
    "n_total",
    "n_segmental",
    "n_global",
    "abnormal_glomeruli",
    "chronic_change",
    "transplant",
    "diagnosis"
]

global_config_path = "config/global_config.yaml"
global_config = load_global_config(global_config_path)

default_config_path = "config/experimental_config.yaml"
experimental_config = load_experimental_config(default_config_path)

# Initialize the session state once at the start of the app
if "initialized" not in st.session_state:
    st.session_state["initialized"] = True
    # Get data using the path passed into streamlit
    parser = argparse.ArgumentParser()
    parser.add_argument("--d", "--data", type=str)

    args = parser.parse_args()
    data_path = args.d

    # Read data
    with open(data_path) as file:
        st.session_state["data"] = json.load(file)

    # Initialize empty annotations for each document with predefined labels
    for i in range(len(st.session_state["data"])):
        st.session_state[i + 1] = {label: [] for label in PREDEFINED_LABELS}

data = st.session_state["data"]

def update():
    """
    This updates the streamlit app with the most up to date information.
    """
    # Load the temporary session state
    temp = st.session_state["temp"]
    st.session_state[temp["id"]] = temp["annotations"]

    if isinstance(temp["annotations"], dict):
        # Ensure all predefined labels exist in annotations
        for label in PREDEFINED_LABELS:
            if label not in temp["annotations"]:
                temp["annotations"][label] = []

        # Add any new labels to all documents
        for i in range(len(data)):
            for label in PREDEFINED_LABELS:
                if label not in st.session_state[i + 1]:
                    st.session_state[i + 1][label] = []

def save_annotations():
    """
    Saves the annotated text to a JSON file locally.
    """
    annotations_to_save = {}
    for i in range(len(data)):
        annotations_to_save[i + 1] = st.session_state[i + 1]

    output_dir = "annotations_output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "annotations.json")

    with open(output_path, "w") as f:
        json.dump(annotations_to_save, f, indent=2)

    st.success(f"Annotations saved to {output_path}")

def annotation_tool(data: dict):
    """Builds the annotation tool with Streamlit.

    Args:
        data (dict): Dictionary containing the text data
    """
    st.title("NER Annotation Tool")
    
    # Initialize the current report index in session state if not present
    if 'current_report_index' not in st.session_state:
        st.session_state.current_report_index = 1

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous Report"):
            if st.session_state.current_report_index > 1:
                st.session_state.current_report_index -= 1
    
    with col3:
        if st.button("Next Report ➡️"):
            if st.session_state.current_report_index < len(data):
                st.session_state.current_report_index += 1
    
    # Initialise slider using the current report index
    slider_id = st.slider(
        "Select Clinician Note",
        1,
        len(data),
        value=st.session_state.current_report_index,
        on_change=update,
        key="my_slider",
    )
    
    # Update the current report index when slider changes
    st.session_state.current_report_index = slider_id

    string = data[slider_id - 1]
    labels = st.session_state[slider_id]

    # Show available labels
    st.markdown("### Available Labels")
    # st.write(", ".join(PREDEFINED_LABELS))

    # Add CSS to increase text size in the text labeler
    st.markdown(
        f"""
        <style>
        /* Target the main text area in text_labeler */
        .text-labeling-widget {{
            font-size: {12}px !important;
        }}
        .labeled-text {{
            font-size: {12}px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Pass the string and labels into the annotation tool
    annotations = text_labeler(string.replace("\n", "  "), labels)

    # Update temporary session state
    st.session_state["temp"] = {"id": slider_id, "annotations": annotations}

    # Create buttons
    col1, col2 = st.columns(2)
    with col1:
        NER = st.button("NER :mag:")
    with col2:
        save = st.button("Save Annotations")

    if NER:
        update()
        extract()
        update()
        st.experimental_rerun()

    if save:
        update()
        save_annotations()

    # Display current annotations
    if st.checkbox("Show Current Annotations"):
        st.json(labels)

def extract():
    """Uses NER to extract entities."""
    # Load temporary session state
    temp = st.session_state["temp"]

    # Check if the annotations are a dictionary
    if isinstance(temp["annotations"], dict):
        experimental_config.extraction.entity_list = PREDEFINED_LABELS

        string = data[temp["id"] - 1]
        # Run extraction
        results = Extraction(
            global_config=global_config,
            extractionconfig=experimental_config.extraction,
            llm_input=[string.replace("\n", "  ")],
        ).run_or_load(save=False)

        for r in results:
            entities = r["Entities"]
            # Format entity into correct format
            for entity in entities:
                a = {
                    "start": entity["start"],
                    "end": entity["end"],
                    "label": entity["text"],
                }

                # Add new entities to session state if they match predefined labels
                if entity["label"] in PREDEFINED_LABELS:
                    if a not in st.session_state[temp["id"]][entity["label"]]:
                        st.session_state[temp["id"]][entity["label"]].append(a)

    print("Extraction Done")
    return None

annotation_tool(data)

verbose = False
if verbose:
    st.write(st.session_state)