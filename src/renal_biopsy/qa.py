from typing import Dict, Any, List

from modelling.qa_base import OllamaQA, LlamaCppQA
from src.renal_biopsy.few_shots import few_shots_list


class RenalBiopsyOllamaQA(OllamaQA):
    """QA model for renal biopsy analysis using Ollama backend."""
    
    def get_report_string(self, report: Dict[str, str]) -> str:
        return f"""MICROSCOPY SECTION: {report['microscopy_section']}
        CONCLUSION SECTION: {report['conclusion_section']}
        """
    
    def get_few_shot_list(self) -> List[str]:
        return few_shots_list


class RenalBiopsyLlamaCppQA(LlamaCppQA):
    """QA model for renal biopsy analysis using LlamaCpp backend."""
    
    def get_report_string(self, report: Dict[str, str]) -> str:
        return f"""MICROSCOPY SECTION: {report['microscopy_section']}
        CONCLUSION SECTION: {report['conclusion_section']}
        """
    
    def get_few_shot_list(self) -> List[str]:
        return few_shots_list
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {
                    "cortex_present": {"type": "boolean"},
                    "medulla_present": {"type": "boolean"},
                    "n_total": {"type": "integer"},
                    "n_segmental": {"type": "numerical"},
                    "n_global": {"type": "numerical"},
                    "abnormal_glomeruli": {"type": "boolean"},
                    "chronic_change": {"type": "string"},
                    "transplant": {"type": "boolean"},
                    "diagnosis": {"type": "string"}
                }
            }
        }