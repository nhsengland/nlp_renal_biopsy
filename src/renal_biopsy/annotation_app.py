import argparse
import streamlit as st
from typing import Dict, Any

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from preprocessing.annotation_app_base import StreamlitAppBase


class RenalBiopsyStreamlitApp(StreamlitAppBase):
    """
    Streamlit app for annotating renal biopsy medical reports.
    Displays microscopy and conclusion sections for annotation.
    
    Run from src directory: 
    streamlit run renal_biopsy/annotation_app.py renal_biopsy renal_biopsy/data/real_input.json
    """
    
    def write_report_string_for_streamlit(self, report: Dict[str, Any]) -> None:
        """
        Display the renal biopsy report in Streamlit.
        Displays microscopy and conclusion sections.
        
        Args:
            report: Dictionary containing the report sections
        
        Note:
            Report format must match get_report_string() in qa.py
        """
        st.subheader("Microscopy Section")
        st.write(report['microscopy_section'])
        
        st.subheader("Conclusion Section")
        st.write(report['conclusion_section'])


def main():
    parser = argparse.ArgumentParser(description="Renal biopsy report annotation tool")
    parser.add_argument(
        "root_dir",
        help="Root directory for data modality",
        type=str
    )
    parser.add_argument(
        "input_path",
        help="Path to input JSON file for annotation",
        type=str
    )
    
    args = parser.parse_args()
    app = RenalBiopsyStreamlitApp(args.root_dir, args.input_path)
    app.run()


if __name__ == "__main__":
    main()