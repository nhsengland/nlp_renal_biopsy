"""
Utilities for handling JSON data and LLM output processing.
Provides functionality for loading, saving, and converting JSON data,
particularly focused on processing LLM-generated outputs.
"""

import json
import copy
import re
from typing import Any, Dict, List, Union
from pathlib import Path


def load_json(file_path: Union[str, Path]) -> Any:
    """
    Load and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON content
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_json(data: Any, path: Union[str, Path], indent: int = 4) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save (must be JSON-serializable)
        path: Output file path
        indent: Number of spaces for indentation
        
    Raises:
        OSError: If there's an error writing the file
        TypeError: If the data is not JSON-serializable
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent)


def parse_json_string(input_string: str) -> Dict[str, Any]:
    """
    Parse a string containing a JSON dictionary, handling common formatting issues.
    
    Args:
        input_string: String containing JSON data
        
    Returns:
        Parsed dictionary
        
    Raises:
        ValueError: If the input can't be parsed as valid JSON
    """
    try:
        # Find the outermost JSON dictionary
        start_index = input_string.find('{')
        end_index = input_string.rfind('}') + 1
        
        if start_index == -1 or end_index == 0:
            raise ValueError("No JSON dictionary found in input string")
            
        json_string = input_string[start_index:end_index]
        
        # Ensure dictionary keys are properly quoted
        json_string = re.sub(r'([{,])\s*([^":\s]+)\s*:', r'\1 "\2":', json_string)
        
        return json.loads(json_string)
        
    except (json.JSONDecodeError, IndexError) as e:
        raise ValueError(f"Failed to parse JSON string: {str(e)}") from e


def process_llm_response(
    generated_report: Union[Dict[str, Any], str],
    report_template: Dict[str, Any],
    keys_to_extract: List[str]
) -> Dict[str, Any]:
    """
    Process a single LLM response and extract specified keys.
    
    Args:
        generated_report: Raw LLM response (either a dictionary with 'response' key or direct string)
        report_template: Template dictionary to fill
        keys_to_extract: Keys to extract from the LLM response
        
    Returns:
        Updated report with extracted values
    """
    processed_report = copy.deepcopy(report_template)
    
    try:
        # Handle both string and dictionary inputs
        response_text = generated_report['response'] if isinstance(generated_report, dict) else generated_report
        response_content = parse_json_string(response_text)
        
        for key in keys_to_extract:
            if key in response_content:
                processed_report[key] = str(response_content[key])
    except (KeyError, ValueError) as e:
        print(f"Error processing LLM response: {e}")
        print(f"Raw response: {generated_report}")
        
    return processed_report


def process_llm_batch(
    generated_answers: List[Dict[str, Any]],
    input_template: List[Dict[str, Any]],
    keys_to_extract: List[str],
    batch_size: int = 2,
    use_llama_cpp: bool = True
) -> List[Dict[str, Any]]:
    """
    Process a batch of LLM responses and extract specified keys.
    
    Args:
        generated_answers: List of raw LLM responses
        input_template: Template for the output structure
        keys_to_extract: Keys to extract from each response
        batch_size: Number of responses to process
        use_llama_cpp: Whether to use llama.cpp response format
        
    Returns:
        List of processed reports
    """
    results = copy.deepcopy(input_template[:batch_size])
    
    for i, (answer, template) in enumerate(zip(generated_answers, results)):
        try:
            if use_llama_cpp:
                content = json.loads(answer['choices'][0]['message']['content'])
                for key in keys_to_extract:
                    if key in content:
                        template[key] = content[key]
            else:
                template = process_llm_response(answer, template, keys_to_extract)
                results[i] = template
        except (KeyError, json.JSONDecodeError, ValueError) as e:
            print(f"Error processing batch item {i}: {e}")
            
    return results