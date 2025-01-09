from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import json
from .guidelines import EntityGuidelines

class MedicalReportProcessor(ABC):
    """Base class for processing medical reports."""
    
    def __init__(self, headers: List[str], guidelines: EntityGuidelines):
        """
        Initialise the report processor.
        
        Args:
            headers: List of section headers to extract from reports
            guidelines: EntityGuidelines instance containing entity information
        """
        self.headers = headers
        self.guidelines = guidelines
    
    def create_input_json(
        self,
        data_path: str,
        save_path: Optional[str] = None,
        full: bool = True
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Create input JSON from processed reports.
        
        Args:
            data_path: Path to input data file
            save_path: Optional path to save JSON output
            full: Whether to use full processing mode
            
        Returns:
            Dictionary containing processed reports
        """
        segmented_reports = (
            self.process_all_reports_real(data_path)
            if full
            else self.process_all_reports(data_path)
        )
        
        input_json = []
        for report in segmented_reports:
            report_entry = self._create_report_entry(
                report=report,
                entity_to_info_map=self.guidelines.entity_to_info_map
            )
            input_json.append(report_entry)
        
        if save_path:
            with open(save_path, 'w') as f:
                json.dump(input_json, f, indent=4)
                
        return input_json
    
    def extract_valid_sections(
        self,
        reports: List[Dict[str, str]],
        required_sections: Optional[List[str]] = None
    ) -> tuple[List[Dict[str, str]], List[str], ...]:
        """
        Extract reports and their sections where all required sections are present.
        
        Args:
            reports: List of report dictionaries
            required_sections: List of section names that must be present and non-None.
                           Defaults to processor's essential sections if None.
            
        Returns:
            Tuple containing (filtered reports, lists of each required section's content)
            
        Example:
            filtered_reports, microscopy_sections, conclusion_sections = (
                processor.extract_valid_sections(reports, ['MICROSCOPY', 'CONCLUSION'])
            )
        """
        # Use default required sections if none provided
        required_sections = required_sections or ['MICROSCOPY', 'CONCLUSION']
        
        # Filter reports where all required sections are present
        valid_reports = [
            report for report in reports 
            if all(report.get(section) is not None for section in required_sections)
        ]
        
        # Extract each section's content
        section_contents = [
            [report[section] for report in valid_reports]
            for section in required_sections
        ]
        
        return (valid_reports, *section_contents)
    
    @abstractmethod
    def _create_report_entry(
        self,
        report: Dict[str, str],
        entity_to_info_map: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a single report entry."""
        pass
    
    @abstractmethod
    def process_all_reports_real(self, file_path: str) -> List[Dict[str, str]]:
        """Process reports in full mode."""
        pass
    
    @abstractmethod
    def process_all_reports(self, file_path: str) -> List[Dict[str, str]]:
        """Process reports in basic mode."""
        pass
    
    @abstractmethod
    def segment_report(self, text: str) -> Dict[str, str]:
        """Segment a report into sections."""
        pass