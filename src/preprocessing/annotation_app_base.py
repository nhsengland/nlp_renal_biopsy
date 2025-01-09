import streamlit as st
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List

from .guidelines import EntityGuidelines
from utils.json import load_json
from utils.general import insert_newlines


class StreamlitAppBase(ABC):
    """Base class for medical report annotation apps using Streamlit."""
    
    CUSTOM_CSS = """
        <style>
            body { font-size: 14px; }
            .question { margin-top: 20px; margin-bottom: -30px; }
            h1 { font-size: 18px; }
            h2 { font-size: 12px; font-weight: bold; }
            h3 { font-size: 16px; }
        </style>
    """
    
    def __init__(self, root_dir: str | Path, input_path: str | Path):
        """
        Initialise the annotation app.
        
        Args:
            root_dir: Root directory containing project files
            input_path: Path to input JSON file for annotation
        """
        self.root_dir = Path(root_dir)
        self.input_path = Path(input_path)
        self.guidelines = EntityGuidelines(self.root_dir / "data/guidelines.xlsx")
    
    def run(self) -> None:
        """Run the Streamlit annotation app."""
        st.title("Medical Report Question Answering")
        st.markdown(self.CUSTOM_CSS, unsafe_allow_html=True)
        
        if not self.input_path.exists():
            st.error(f"File {self.input_path} not found.")
            return
            
        self._initialise_session()
        self._setup_interface()
    
    def _initialise_session(self) -> None:
        """Initialise Streamlit session state."""
        reports = load_json(self.input_path)
        
        if 'answers' not in st.session_state:
            st.session_state['answers'] = reports.copy()
        if 'current_report_index' not in st.session_state:
            st.session_state['current_report_index'] = 0
    
    def _setup_interface(self) -> None:
        """Set up the main interface components."""
        # Filter controls
        filter_clinician = st.checkbox("Show only reports for clinician review", value=False)
        filtered_reports = self._get_filtered_reports(filter_clinician)
        
        if not filtered_reports:
            st.warning("No reports found.")
            return
            
        # Navigation controls
        current_index = self._setup_navigation(filtered_reports)
        current_report = filtered_reports[current_index]
        
        # Display report and questions
        self.write_report_string_for_streamlit(current_report)
        st.write("-----")
        st.subheader("Questions")
        
        answers = self._create_question_interface(
            current_report, 
            current_index, 
            self.guidelines.entity_to_info_map
        )
        
        # Setup save controls
        self._setup_save_controls(current_report, answers, current_index, filtered_reports)
    
    def _get_filtered_reports(self, filter_clinician: bool) -> List[Dict[str, Any]]:
        """Get filtered list of reports based on clinician check status."""
        if filter_clinician:
            return [r for r in st.session_state['answers'] if r.get("clinician_check") == "True"]
        return st.session_state['answers']
    
    def _setup_navigation(self, reports: List[Dict[str, Any]]) -> int:
        """Set up navigation controls and return current index."""
        current_index = st.slider(
            "Select Report",
            0, len(reports) - 1,
            st.session_state['current_report_index']
        )
        
        col1, col2 = st.columns([2, 1])
        with col1:
            jump_to = st.number_input(
                "Enter report number",
                0, len(reports) - 1,
                current_index,
                key="jump_to_report"
            )
        with col2:
            if st.button("Jump to Report"):
                if 0 <= jump_to < len(reports):
                    st.session_state['current_report_index'] = jump_to
                    st.rerun()
                else:
                    st.error(f"Invalid report number. Must be 0-{len(reports)-1}")
        
        st.session_state['current_report_index'] = current_index
        return current_index
    
    def _create_question_interface(
        self,
        report: Dict[str, Any],
        index: int,
        entity_map: Dict[str, tuple]
    ) -> Dict[str, str]:
        """Create question interface and return answers."""
        answers = {}
        
        for entity_code, (question, type_, guidelines) in entity_map.items():
            tooltip = f"<div class='question'>{question} <span title='{insert_newlines(guidelines)}' style='color:blue; cursor: help;'>[?]</span></div>"
            st.markdown(tooltip, unsafe_allow_html=True)
            
            if type_ == 'boolean':
                value = st.radio(
                    "",
                    ["True", "False"],
                    index=0 if report.get(entity_code, "") == "True" else 1,
                    key=f'answer_{index}_{entity_code}',
                    horizontal=True
                )
            elif type_ == 'categorical':
                # TODO: Implement dropdown
                continue
            else:
                value = st.text_input(
                    "",
                    value=report.get(entity_code, ""),
                    key=f'answer_{index}_{entity_code}'
                )
            answers[entity_code] = value
        
        clinician_check = st.radio(
            "Requires clinician review?",
            ["True", "False"],
            index=0 if report.get('clinician_check', "") == "True" else 1,
            key=f'answer_{index}_clinician_check',
            horizontal=True
        )
        answers["clinician_check"] = clinician_check
        
        return answers
    
    def _setup_save_controls(
        self,
        report: Dict[str, Any],
        answers: Dict[str, str],
        index: int,
        reports: List[Dict[str, Any]]
    ) -> None:
        """Set up save and navigation controls."""
        def save_state(path: str | Path) -> None:
            updated = {**report, **answers}
            st.session_state['answers'][index] = updated
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                json.dump(st.session_state['answers'], f, indent=4)
        
        st.markdown("Navigation buttons save automatically")
        if st.button("Save Answers"):
            save_state(self.root_dir / "data/real_output.json")
            st.success("Saved to data/real_output.json")
        
        # Navigation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Report") and index > 0:
                save_state(self.root_dir / "data/real_output.json")
                st.session_state['current_report_index'] -= 1
                st.rerun()
        
        with col2:
            if st.button("Next Report"):
                save_state(self.root_dir / "data/real_output.json")
                if index < len(reports) - 1:
                    st.session_state['current_report_index'] += 1
                    st.rerun()
                else:
                    st.warning("Last report reached")
        
        # Custom save path
        st.markdown("<br>", unsafe_allow_html=True)
        save_path = st.text_input(
            "Save copy with custom name (helpful before closing Streamlit):",
            "src/renal_biopsy/data/output_report_temp.json"
        )
        
        if st.button("Save Custom Copy"):
            save_state(save_path)
            st.success(f"Saved to {save_path}")
    
    @abstractmethod
    def write_report_string_for_streamlit(self, report: Dict[str, Any]) -> None:
        """Display the report in Streamlit. Must be implemented by subclasses."""
        pass