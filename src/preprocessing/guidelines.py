import pandas as pd
from typing import Dict, Tuple


class EntityGuidelines:
    """
    Processes entity guidelines from Excel files to create mappings and schemas.
    
    The class reads an Excel file containing entity guidelines and creates:
    - A mapping of entity codes to their information
    - A DataFrame of guidelines for prompts
    - A JSON schema for LLaMA-cpp format
    """
    
    def __init__(self, path: str):
        """
        Initialise EntityGuidelines with the path to the guideline.xlsx file.

        Args:
            path: Path to the Excel file containing entity guidelines
        """
        self.path = path
        self.entity_to_info_map = self.create_entity_to_info_map()
        self.prompt_df = self.get_guidelines_info_for_prompt()
        self.json_schema = self.create_llama_cpp_json_schema()
    
    def create_entity_to_info_map(self) -> Dict[str, Tuple[str, str, str]]:
        """
        Create a mapping of entity codes to their associated information.
        
        Returns:
            Dictionary mapping entity codes to tuples containing:
            (entity question, entity type, entity guidelines)
        """
        df = pd.read_excel(self.path, header=0, index_col=None)
        df = df.drop(index=0)  # drop header explainer row
        df['Entity Guidelines'] = df['Entity Guidelines'].fillna('')  # handle empty guidelines
        
        entity_to_info_map = df.set_index('Entity Code')[
            ['Entity Question To Ask', 'Entity Type', 'Entity Guidelines']
        ].to_dict(orient='index')
        
        return {
            k: (v['Entity Question To Ask'], v['Entity Type'], v['Entity Guidelines'])
            for k, v in entity_to_info_map.items()
        }
    
    def get_guidelines_info_for_prompt(self) -> pd.DataFrame:
        """
        Process guidelines information for prompts.
        
        If combined questions/guidelines don't exist, uses individual entity
        questions and guidelines instead.

        Returns:
            DataFrame containing entity codes and their associated prompt information
        """
        df = pd.read_excel(self.path, header=0, index_col=None)
        df = df.drop(index=0)  # drop header explainer row
        
        # If no combined questions exist, use individual entity questions
        if df['Combined Prompt Question'].isnull().all() and df['Combined Guidelines'].isnull().all():
            df['Combined Prompt Question'] = df['Entity Question To Ask']
            df['Combined Guidelines'] = df['Entity Guidelines']
            
        prompt_df = df[['Entity Code', 'Combined Prompt Question', 'Combined Guidelines']]
        return prompt_df.dropna(how='all')
    
    def create_llama_cpp_json_schema(self) -> dict:
        """
        Create a JSON schema in LLaMA-cpp format.
        
        Returns:
            Dictionary containing the JSON schema with entity types as properties
        """
        json_schema = {
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {
                    k: {"type": v[1]} 
                    for k, v in self.entity_to_info_map.items()
                }
            }
        }
        return json_schema