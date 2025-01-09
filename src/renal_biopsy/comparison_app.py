import streamlit as st
import json
from typing import Tuple, List, Dict, Any

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from preprocessing.guidelines import EntityGuidelines
from utils.general import insert_newlines

class RenalBiopsyComparisonApp:
    def __init__(self, root_dir: str):
        """Initialise the comparison app with necessary paths."""
        self.root_dir = root_dir
        self.entity_guidelines = EntityGuidelines(f"{root_dir}/data/guidelines.xlsx")
        self.entity_to_info_map = self.entity_guidelines.create_entity_to_info_map()
        
        # Initialise comments in session state if not exists
        if 'comments' not in st.session_state:
            st.session_state.comments = {}
    
    def load_and_validate_predictions(self, pred1_path: str, pred2_path: str, matches_path: str, n_prototype: int) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, bool]]]:
        """Load and validate prediction files and matches."""
        try:
            with open(pred1_path) as f1, open(pred2_path) as f2, open(matches_path) as f3:
                pred1_reports = json.load(f1)[:n_prototype]  # Limit to n_prototype
                pred2_reports = json.load(f2)[:n_prototype]  # Limit to n_prototype
                matches = json.load(f3)
            
            # Validate basic structure
            if not all(isinstance(x, list) for x in [pred1_reports, pred2_reports, matches]):
                raise ValueError("All input files must contain a list of reports")
                
            if not all(len(x) > 0 for x in [pred1_reports, pred2_reports, matches]):
                raise ValueError("Input files cannot be empty")
                
            if not len(pred1_reports) == len(pred2_reports) == len(matches):
                raise ValueError(f"Number of reports doesn't match: {len(pred1_reports)} vs {len(pred2_reports)} vs {len(matches)}")
            
            # Validate matches format
            for i, match_dict in enumerate(matches):
                if not isinstance(match_dict, dict):
                    raise ValueError(f"Match {i} is not a dictionary")
                if not all(isinstance(v, bool) for v in match_dict.values()):
                    raise ValueError(f"Match {i} contains non-boolean values")
                    
            return pred1_reports, pred2_reports, matches
                
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error loading files: {str(e)}")
    
    def setup_page(self):
        """Configure Streamlit page settings and styles."""
        st.set_page_config(
            layout="wide",
            initial_sidebar_state="collapsed",
            menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
        )
        
        st.markdown("""
            <style>
                .reportview-container .main .block-container {
                    max-width: 1400px;
                    padding: 1rem;
                }
                
                /* Question styling */
                .question { 
                    margin-top: 30px;
                    margin-bottom: 20px;
                    font-weight: bold;
                    font-size: 22px;  /* Increased from 15px */
                    line-height: 1.4;
                }
                
                /* Text area styling */
                .stTextArea textarea {
                    min-height: 120px !important;  /* Increased from 100px */
                    font-size: 24px !important;    /* Added font size */
                    line-height: 1.4 !important;   /* Added line height */
                    padding: 12px !important;      /* Added padding */
                }
                
                /* Radio button styling */
                .stRadio > div {
                    gap: 2rem !important;          /* Increased gap between options */
                }
                
                .stRadio label {
                    font-size: 24px !important;    /* Increased font size */
                    padding: 8px !important;       /* Added padding */
                }
                
                /* Button styling */
                .stButton button {
                    width: 100%;
                    font-size: 24px !important;    /* Increased font size */
                    padding: 10px 24px !important; /* Increased padding */
                    height: auto !important;       /* Allow button height to adjust */
                }
                
                /* Hide Streamlit elements */
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                
                /* Remove label spacing */
                .stRadio > label { display: none; }
                .stTextInput > label { display: none; }
                
                /* Report sections */
                .report-section {
                    border: 1px solid #ddd;
                    padding: 15px;                 /* Increased padding */
                    border-radius: 5px;
                    margin-bottom: 15px;
                    background-color: white;
                    font-size: 20px;              /* Added font size */
                    line-height: 1.5;             /* Added line height */
                }
                
                /* Navigation elements */
                .stSlider div[data-baseweb="slider"] {
                    height: 20px !important;      /* Made slider bigger */
                }
                
                .stNumberInput input {
                    font-size: 16px !important;   /* Increased input font size */
                    padding: 8px 12px !important; /* Added padding */
                }
                
                /* Section headers */
                h5 {
                    font-size: 20px !important;   /* Increased header size */
                    margin-bottom: 15px !important;
                }
                
                /* Summary section */
                .markdown-text-container {
                    font-size: 20px !important;   /* Increased summary text size */
                    line-height: 1.5 !important;
                }
            </style>
        """, unsafe_allow_html=True)

    def setup_page_orig(self):
        """Configure Streamlit page settings and styles."""
        st.set_page_config(
            layout="wide",
            initial_sidebar_state="collapsed",
            menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
        )
        
        st.markdown("""
            <style>
                .reportview-container .main .block-container {
                    max-width: 1400px;
                    padding: 1rem;
                }
                .question { 
                    margin-top: 20px;
                    margin-bottom: 15px;
                    font-weight: bold;
                    font-size: 15px;
                }
                .stTextArea textarea {
                    min-height: 100px !important;
                }
                
                /* Hide Streamlit elements */
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                
                /* Remove label spacing */
                .stRadio > label { display: none; }
                .stTextInput > label { display: none; }
                
                /* Report sections */
                .report-section {
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 10px;
                    background-color: white;
                }
                
                /* Navigation buttons */
                .stButton button {
                    width: 100%;
                }
            </style>
        """, unsafe_allow_html=True)

    def save_comments(self, comments: Dict, filename: str = "comparison_comments.json"):
        """Save comments to a JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(comments, f, indent=4)
            st.success(f"Comments saved to {filename}")
        except Exception as e:
            st.error(f"Error saving comments: {str(e)}")

    def display_reports(self, pred1: Dict[str, Any], pred2: Dict[str, Any]):
        """Display two reports side by side."""
        container = st.container()
        with container:
            _, center_col, _ = st.columns([1, 4, 1])
            with center_col:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("##### Model 1 Prediction")
                    with st.container():
                        st.markdown("**Microscopy Section**")
                        st.markdown(f"<div class='report-section'>{pred1.get('microscopy_section', '')}</div>", 
                                  unsafe_allow_html=True)
                        st.markdown("**Conclusion Section**")
                        st.markdown(f"<div class='report-section'>{pred1.get('conclusion_section', '')}</div>", 
                                  unsafe_allow_html=True)
                
                with col2:
                    st.markdown("##### Model 2 Prediction")
                    with st.container():
                        st.markdown("**Microscopy Section**")
                        st.markdown(f"<div class='report-section'>{pred2.get('microscopy_section', '')}</div>", 
                                  unsafe_allow_html=True)
                        st.markdown("**Conclusion Section**")
                        st.markdown(f"<div class='report-section'>{pred2.get('conclusion_section', '')}</div>", 
                                  unsafe_allow_html=True)

    def display_comparison_questions(self, pred1: Dict[str, Any], pred2: Dict[str, Any], 
                                  matches: Dict[str, bool], current_index: int) -> Dict[str, Any]:
        """Display questions and answers for both predictions side by side with comments."""
        answers = {}
        
        container = st.container()
        with container:
            _, center_col, _ = st.columns([1, 4, 1])
            with center_col:
                for entity_code, (question, entity_type, guidelines) in self.entity_to_info_map.items():
                    st.markdown(
                        f"<div class='question'>{question} "
                        f"<span title='{insert_newlines(guidelines)}' "
                        f"style='color:blue; cursor:help;'>[?]</span></div>",
                        unsafe_allow_html=True
                    )
                    
                    col1, col2, col3, col4 = st.columns([4, 4, 1, 3])
                    
                    def create_input(col, value, prefix, entity_type):
                        with col:
                            if entity_type == 'boolean':
                                return st.radio(
                                    "##",
                                    ["True", "False"],
                                    index=0 if str(value).lower() == "true" else 1,
                                    key=f'{prefix}_{current_index}_{entity_code}',
                                    horizontal=True,
                                    label_visibility="collapsed"
                                )
                            return st.text_area(
                                "##",
                                value=str(value) if value is not None else "",
                                key=f'{prefix}_{current_index}_{entity_code}',
                                label_visibility="collapsed"
                            )
                    
                    # Create inputs for both predictions
                    answer1 = create_input(col1, pred1.get(entity_code, ""), "pred1", entity_type)
                    answer2 = create_input(col2, pred2.get(entity_code, ""), "pred2", entity_type)
                    
                    # Show match indicator from matches file
                    with col3:
                        match_value = matches.get(entity_code, False)  # Direct boolean value
                        st.markdown(
                            f"<div style='margin-top: 10px; text-align: center;'>"
                            f"<span style='color: {'green' if match_value else 'red'}; "
                            f"font-weight: bold;'>{'✓' if match_value else '✗'}</span></div>",
                            unsafe_allow_html=True
                        )
                    
                    # Add comment box
                    with col4:
                        report_id = f"report_{current_index}"
                        if report_id not in st.session_state.comments:
                            st.session_state.comments[report_id] = {}
                        
                        comment = st.text_area(
                            "Comment",
                            value=st.session_state.comments[report_id].get(entity_code, {}).get('comment', ''),
                            key=f'comment_{current_index}_{entity_code}',
                            label_visibility="collapsed"
                        )
                        
                        # Store comment in session state
                        if comment:
                            st.session_state.comments[report_id][entity_code] = {
                                'pred1': answer1,
                                'pred2': answer2,
                                'match': match_value,
                                'comment': comment
                            }
                    
                    st.markdown("<div style='margin-bottom: 20px'></div>", 
                              unsafe_allow_html=True)
                    
                    answers[f"{entity_code}_1"] = answer1
                    answers[f"{entity_code}_2"] = answer2
        
        return answers

    def display_summary(self, matches: Dict[str, bool]):
        """Display summary statistics of the comparison."""
        _, center_col, _ = st.columns([1, 4, 1])
        with center_col:
            st.write("-----")
            st.subheader("Comparison Summary")
            
            total = len(matches)
            matching = sum(1 for value in matches.values() if value)
            match_percent = (matching / total * 100) if total > 0 else 0
            
            st.markdown(f"""
                - Total questions: {total}
                - Matching predictions: {matching}
                - Match percentage: {match_percent:.1f}%
            """)
    
    def run(self, pred1_path: str, pred2_path: str, matches_path: str, n_prototype: int = 100):
        """Run the comparison app."""
        self.setup_page()
        st.title("Model Predictions Comparison")

        try:
            pred1_reports, pred2_reports, matches = self.load_and_validate_predictions(
                pred1_path, pred2_path, matches_path, n_prototype
            )
        except ValueError as e:
            st.error(str(e))
            return

        total_reports = len(pred1_reports)
        
        # Navigation controls at top
        col1, col2 = st.columns([3, 1])
        with col1:
            current_index = st.slider(
                "Select Report",
                0, total_reports - 1,
                st.session_state.get('current_report_index', 0)
            )
        with col2:
            jump_to = st.number_input(
                "Jump to report",
                min_value=0,
                max_value=total_reports - 1,
                value=current_index,
                step=1
            )
            if st.button("Go"):
                current_index = jump_to
                
        st.session_state['current_report_index'] = current_index

        # Display current reports and comparison
        current_pred1 = pred1_reports[current_index]
        current_pred2 = pred2_reports[current_index]
        current_matches = matches[current_index]
        
        self.display_reports(current_pred1, current_pred2)
        st.write("-----")
        
        st.subheader("Comparison Questions")
        answers = self.display_comparison_questions(
            current_pred1, current_pred2, current_matches, current_index
        )
        
        self.display_summary(current_matches)
        
        # Navigation buttons at bottom
        st.write("-----")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Previous Report"):
                if current_index > 0:
                    st.session_state['current_report_index'] = current_index - 1
                    st.rerun()
        with col3:
            if st.button("Next Report →"):
                if current_index < total_reports - 1:
                    st.session_state['current_report_index'] = current_index + 1
                    st.rerun()
        
        # Save comments button
        st.write("-----")
        save_path = st.text_input("Save comments to file:", "comparison_comments.json")
        if st.button("Save All Comments"):
            self.save_comments(st.session_state.comments, save_path)

if __name__ == "__main__":
    import sys
    import os
    
    # Get command line arguments
    if len(sys.argv) < 3:
        print("Usage: streamlit run comparison_app.py <root_dir> <run_dir> [n_prototype]")
        sys.exit(1)
        
    root_dir = sys.argv[1]
    run_dir = sys.argv[2]
    n_prototype = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    
    # Construct full paths
    pred1_path = os.path.join(root_dir, run_dir, "model_1_predicted.json")
    pred2_path = os.path.join(root_dir, run_dir, "model_2_predicted.json")
    match_path = os.path.join(root_dir, run_dir, "entity_answers_over_corpus.json")
    
    app = RenalBiopsyComparisonApp(root_dir)
    app.run(pred1_path, pred2_path, match_path, n_prototype)