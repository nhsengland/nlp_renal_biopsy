"""
Medical report QA models using different LLM backends (Ollama and LlamaCpp).
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import pandas as pd
from tqdm import tqdm
import ollama
from llama_cpp import Llama

from src.preprocessing.guidelines import EntityGuidelines
from src.utils.json import process_llm_batch
from src.evaluate.report import evaluate_report


class QABase(ABC):
    """Abstract base class for medical report QA models."""
    
    DEFAULT_SYSTEM_MSG = """
    You are a biomedical expert. Answer the questions below using the JSON dictionary template only. 
    Do not mention anything that is not in the report and do not add any text beyond the JSON.
    """
    
    def __init__(
        self,
        model_path: str,
        root_dir: str,
        system_message: Optional[str] = None
    ):
        """Initialise base QA model."""
        self.model_path = model_path
        self.root_dir = root_dir
        self.system_message = system_message or self.DEFAULT_SYSTEM_MSG
        self.entity_guidelines = EntityGuidelines(f"{root_dir}/data/guidelines.xlsx")
        self.max_n_few_shots = 2
    
    def create_task_prompt(self, n_shots: int = 0, include_guidelines: bool = True) -> str:
        """Create the task prompt with optional few-shot examples."""
        questions = self.get_questions_string()
        guidelines = self.get_entity_guidelines_string() if include_guidelines else ""
        few_shots = self.get_few_shot_list()
        
        if n_shots == 0:
            task = f"""
            Given the real report at the end of this prompt your task is to answer the following questions:
            {questions}
            {self._get_format_instructions()}

            --- GUIDELINES ---
            {guidelines}

            """
            return f"{self.system_message} {task}"
        
        if 0 < n_shots <= self.max_n_few_shots:
            task = f"""
            Given the real report at the end of this prompt and the example reports with answers, your task is to answer the following questions:
            {questions}
            {self._get_format_instructions()}

            --- GUIDELINES ---
            {guidelines}

            """
            shots = "\n".join(few_shots[:n_shots])
            return f"{self.system_message} {task} {shots}"
        
        raise ValueError(f"n_shots must be between 0 and {self.max_n_few_shots}")
    
    def evaluate(
        self,
        annotated_json: List[Dict[str, Any]],
        predicted_json: List[Dict[str, Any]],
        n_prototypes: int = 3
    ) -> tuple:
        """Evaluate model predictions against annotations."""
        e2i_map = self.entity_guidelines.entity_to_info_map
        n_entities = len(e2i_map)
        all_scores = []
        
        for i, (anno, pred) in enumerate(
            tqdm(zip(annotated_json, predicted_json),
                 total=n_prototypes,
                 desc="Evaluating predictions",
                 ncols=110)
        ):
            if i == n_prototypes:
                break
            report_scores = evaluate_report(e2i_map, anno, pred)
            all_scores.append(report_scores)
        
        # Calculate scores
        scores_per_report = [
            round(sum(scores.values()) / n_entities, 3)
            for scores in all_scores
        ]
        
        final_score = round(sum(scores_per_report) / n_prototypes, 3)

        return all_scores, scores_per_report, final_score

    def calculate_entity_accuracy(
        self,
        all_scores: List[Dict[str, float]],
    ) -> Dict:
        """
        Calculate accuracy for each entity from evaluation scores.
        
        Args:
            all_scores: List of dictionaries containing entity scores from evaluate()
            entity_to_info_map: Dictionary mapping entities to their metadata
            
        Returns:
            Dictionary containing accuracy statistics for each entity
        """
        # Initialise results dictionary
        results = {entity: {
            'correct': 0,
            'total': len(all_scores),
        } for entity in self.entity_guidelines.entity_to_info_map.keys()}
                
        # Process all scores
        for report_scores in all_scores:
            for entity, score in report_scores.items():
                results[entity]['correct'] += score
        
        # Calculate percentages
        for entity in results:
            total = results[entity]['total']
            correct = results[entity]['correct']
            results[entity]['accuracy'] = round((correct/total) * 100, 1)
            
        # Print results
        print("\nAccuracy per entity:")
        print("=" * 60)
        print(f"{'Entity':30} {'Score':15} {'Type':15}")
        print("-" * 60)
        
        for entity, scores in results.items():
            entity_type = self.entity_guidelines.entity_to_info_map[entity][1]
            score_str = f"{scores['correct']}/{scores['total']} ({scores['accuracy']}%)"            
            print(f"{entity:30} {score_str:15} {entity_type:15}")
        
        return results
    
    def get_entity_list(self) -> List[str]:
        """Get list of entity codes."""
        return list(self.entity_guidelines.entity_to_info_map.keys())
    
    def get_questions_string(self) -> str:
        """Get concatenated question prompts."""
        return "\n".join(
            self.entity_guidelines.prompt_df['Combined Prompt Question'].dropna()
        )
    
    def get_output_template_string(self) -> str:
        """Get JSON template string."""
        template = "{"
        for entity, (_, entity_type, _) in self.entity_guidelines.entity_to_info_map.items():
            template += f' "{entity}": "{entity_type}",'
        return template.rstrip(",") + "}"
    
    def get_entity_guidelines_string(self) -> str:
        """Get formatted guidelines string."""
        df = self.entity_guidelines.prompt_df
        
        # Group entities by their guidelines
        grouped_entities = {}
        current_codes = []
        current_guideline = None
        
        for _, row in df.iterrows():
            guideline = row['Combined Guidelines']
            code = row['Entity Code']
            
            # If we find a new non-null guideline, start a new group
            if not pd.isna(guideline):
                if current_guideline is not None:
                    # Store the previous group
                    grouped_entities[current_guideline] = current_codes
                # Start new group
                current_codes = [code]
                current_guideline = guideline
            else:
                # Add to current group if we have one
                if current_guideline is not None:
                    current_codes.append(code)
        
        # Add the last group if exists
        if current_guideline is not None and current_codes:
            grouped_entities[current_guideline] = current_codes
            
        # Format the output
        guidelines = []
        for guideline, codes in grouped_entities.items():
            codes_str = ", ".join(codes)
            guidelines.append(f"{codes_str} : {guideline}")
            
        return "\n".join(guidelines)
    
    @abstractmethod
    def _get_format_instructions(self) -> str:
        """Get model-specific format instructions."""
        pass
    
    @abstractmethod
    def get_few_shot_list(self) -> List[str]:
        """Get list of few-shot examples."""
        pass
    
    @abstractmethod
    def get_report_string(self, report: Dict[str, Any]) -> str:
        """Get formatted report string."""
        pass
    
    @abstractmethod
    def extract_with_known_entities(
        self,
        input_json: List[Dict[str, Any]],
        n_shots: int = 0,
        n_prototype: int = 2,
        include_guidelines: bool = True
    ) -> List[Dict[str, Any]]:
        """Extract entities from reports."""
        pass


class OllamaQA(QABase):
    """QA model using Ollama backend."""
    
    def _get_format_instructions(self) -> str:
        return f"TEMPLATE: {self.get_output_template_string()}"
    
    def convert_generated_answers_to_json(
        self,
        generated_answers: List[str],
        input_json: List[Dict[str, Any]],
        n_prototype: int
    ) -> List[Dict[str, Any]]:
        """Convert generated answers to JSON format."""
        entity_list = self.get_entity_list()
        return process_llm_batch(
            generated_answers,
            input_json,
            entity_list,
            n_prototype,
            use_llama_cpp=False
        )
    
    def extract_with_known_entities(
        self,
        input_json: List[Dict[str, Any]],
        n_shots: int = 0,
        n_prototype: int = 2,
        include_guidelines: bool = True
    ) -> List[str]:
        """Extract entities using Ollama."""
        task_prompt = self.create_task_prompt(n_shots, include_guidelines)
        answers = []
        
        for report in tqdm(input_json[:n_prototype],
                          desc="Processing reports",
                          ncols=100):
            prompt = f"""
            {task_prompt}
            --- REAL REPORT ---
            {self.get_report_string(report)}
            """
            response = ollama.generate(
                model=self.model_path,
                prompt=prompt,
                options={'temperature': 0}
            )
            answers.append(response['response'])
        
        return answers


class LlamaCppQA(QABase):
    """QA model using llama.cpp backend."""
    
    def _get_format_instructions(self) -> str:
        """No template needed as using JSON schema."""
        return ""
    
    def extract_with_known_entities(
        self,
        input_json: List[Dict[str, Any]],
        n_shots: int = 0,
        n_prototype: int = 2,
        include_guidelines: bool = True
    ) -> List[Dict[str, Any]]:
        """Extract entities using llama.cpp."""
        task_prompt = self.create_task_prompt(n_shots, include_guidelines)
        schema = self.get_schema()
        answers = []
        
        for i, report in enumerate(input_json):
            if i == n_prototype:
                break
                
            messages = [
                {"role": "assistant", "content": task_prompt},
                {"role": "user", "content": f"""
                --- REAL REPORT ---
                {self.get_report_string(report)}
                """},
            ]
            
            llm = Llama(
                model_path=self.model_path,
                chat_format="chatml",
                verbose=False,
                n_ctx=3000,
            )
            
            answer = llm.create_chat_completion(
                messages=messages,
                response_format=schema,
                max_tokens=None,
                temperature=0,
            )
            answers.append(answer)
        
        entity_list = self.get_entity_list()
        return process_llm_batch(
            answers,
            input_json,
            entity_list,
            n_prototype,
            use_llama_cpp=True
        )
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Get JSON schema for output formatting."""
        pass