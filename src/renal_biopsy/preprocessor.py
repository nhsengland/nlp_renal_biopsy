import pandas as pd
from typing import Dict, List, Any


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from preprocessing.preprocessor_base import MedicalReportProcessor
from preprocessing.guidelines import EntityGuidelines


class RenalBiopsyProcessor(MedicalReportProcessor):
    """Processor for renal biopsy histopathology reports."""
    
    def __init__(self, guidelines: EntityGuidelines):
        """
        Initialise the renal biopsy processor.
        
        Args:
            guidelines: EntityGuidelines instance containing entity information
        """
        headers = ["TYPED", "CLINICAL", "SPECIMEN", "MACROSCOPY", "MICROSCOPY", "CONCLUSION"]
        super().__init__(headers, guidelines)
    
    def _create_report_entry(
        self,
        report: Dict[str, str],
        entity_to_info_map: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a single report entry."""
        report_entry = {
            "microscopy_section": report["MICROSCOPY"],
            "conclusion_section": report["CONCLUSION"]
        }
        
        for key in entity_to_info_map:
            report_entry[key] = ""
            
        report_entry['clinician_check'] = False
        return report_entry
    
    def process_all_reports_real(self, file_path: str) -> List[Dict[str, str]]:
        """Process reports in full mode."""
        sample_data = pd.read_excel(file_path)
        segmented_reports = []
        
        for _, report in sample_data.iterrows():
            report_dict = self.segment_report(report['content'])
            report_dict['entity_key'] = report['entity_key']
            
            if self._is_relevant_renal_specimen(report_dict.get('SPECIMEN')):
                segmented_reports.append(report_dict)
        
        print(f"Number of renal biopsy histopathology reports: {len(sample_data)}")
        print(f"Number of reports after SPECIMEN keyword filtering: {len(segmented_reports)}")
        
        return segmented_reports
    
    def process_all_reports(self, file_path: str) -> List[Dict[str, str]]:
        """Process reports in basic mode."""
        sample_data = pd.read_csv(file_path)
        sample_data_filtered = sample_data[sample_data['item_specialty'] == 'Nephrology']
        segmented_reports = []
        
        for _, report in sample_data_filtered.iterrows():
            report_dict = self.segment_report(report['content'])
            report_dict['entity_key'] = report['entity_key']
            
            if report_dict.get('SPECIMEN') and self._is_relevant_renal_specimen(report_dict['SPECIMEN']):
                segmented_reports.append(report_dict)
        
        print(f"Number of renal biopsy histopathology reports: {len(sample_data_filtered)}")
        print(f"Number of reports after SPECIMEN keyword filtering: {len(segmented_reports)}")
        
        return segmented_reports
    
    def segment_report(self, text: str) -> Dict[str, str]:
        """Segment a report into sections."""
        import re
        import Levenshtein
        
        text = self._add_colon_if_found(text)
        text = text.replace("ELECTRON MICROSCOPY", "[electron microscopy]")
        
        pattern = r'(?P<header>[A-Z0-9]+)[:;]? (?P<content>.*?)\s*(?=[A-Z0-9]+[:;] |$)'
        matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
        
        segmented_report = {header: "" for header in self.headers}
        last_valid_header = None

        for match in matches:
            detected_header = match.group("header").upper()
            content = match.group("content").strip()
            
            closest_match = None
            smallest_distance = float('inf')
            
            for correct_header in self.headers:
                distance = Levenshtein.distance(detected_header, correct_header)
                if distance < smallest_distance:
                    smallest_distance = distance
                    closest_match = correct_header
            
            if smallest_distance <= 2:
                segmented_report[closest_match] = content
                last_valid_header = closest_match
            elif last_valid_header:
                segmented_report[last_valid_header] += f" {detected_header}: {content}"
        
        # Set empty sections to None
        for header in self.headers:
            if segmented_report[header] == "":
                segmented_report[header] = None
        
        # Add additional headers
        segmented_report.update({
            'REPORTED BY': None,
            'AUTHORISED BY': None,
            'SUPPLEMENTARY REPORT': None
        })
        
        # Process conclusion section
        self._process_conclusion_section(segmented_report)
        
        return segmented_report
    
    def _add_colon_if_found(self, text: str) -> str:
        """Add colon to end of header to make segmenting reports easier."""
        words = text.split()
        modified_words = []
        for word in words:
            if word in self.headers:
                modified_words.append(word + ':')
            else:
                modified_words.append(word)
        return ' '.join(modified_words)
    
    def _is_relevant_renal_specimen(self, specimen_text: str) -> bool:
        """Check if specimen is relevant for renal analysis."""
        if not specimen_text:
            return False
        relevant_words = ['kidney', 'renal', 'nephrectomy']
        return any(word in specimen_text.lower() for word in relevant_words)
    
    def _process_conclusion_section(self, report: Dict[str, str]) -> None:
        """Process special sections in the conclusion text."""
        import re
        
        orig_conclusion = report.get("CONCLUSION")
        if not orig_conclusion:
            return
            
        # Process "reported by"
        reported_by_match = re.search(r'reported by (.*)', orig_conclusion, re.IGNORECASE)
        if reported_by_match:
            reported_by_text = reported_by_match.group(1).strip()
            report["CONCLUSION"] = orig_conclusion.replace(reported_by_match.group(0), "").strip()
            report["REPORTED BY"] = reported_by_text
            
            # Check for supplementary report in reported by section
            supplementary_match = re.search(r'supplementary report (.*)', reported_by_text, re.IGNORECASE)
            if supplementary_match:
                supplementary_text = supplementary_match.group(1).strip()
                report['REPORTED BY'] = reported_by_text.replace(supplementary_match.group(0), "").strip()
                report['SUPPLEMENTARY REPORT'] = supplementary_text
        
        # Process "authorised by"
        authorised_by_match = re.search(r'report authorised by (.*)', orig_conclusion, re.IGNORECASE)
        if authorised_by_match:
            authorised_text = authorised_by_match.group(1).strip()
            report["CONCLUSION"] = report["CONCLUSION"].replace(authorised_by_match.group(0), "").strip()
            report["AUTHORISED BY"] = authorised_text
        
        # Check for supplementary report in conclusion if not found in reported by
        if not report.get('SUPPLEMENTARY REPORT'):
            supplementary_match = re.search(r'supplementary report (.*)', orig_conclusion, re.IGNORECASE)
            if supplementary_match:
                supplementary_text = supplementary_match.group(1).strip()
                report['CONCLUSION'] = report['CONCLUSION'].replace(supplementary_match.group(0), "").strip()
                report['SUPPLEMENTARY REPORT'] = supplementary_text