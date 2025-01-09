import argparse
import os
import shutil
from datetime import datetime
from pathlib import Path

from src.preprocessing.guidelines import EntityGuidelines
from src.renal_biopsy.preprocessor import RenalBiopsyProcessor
from src.utils.json import load_json, save_json
from src.utils.general import write_metadata_file
from renal_biopsy.qa import RenalBiopsyOllamaQA, RenalBiopsyLlamaCppQA

# Example usage:
# Ollama: python rb_script.py --backend ollama --root_dir src/renal_biopsy --model_name phi3.5:3.8b-mini-instruct-q4_K_M --n_shots 2 --n_prototype 1 --include_guidelines
# Ollama (diff model): python rb_script.py --backend ollama --root_dir src/renal_biopsy --model_name qwen2.5:1.5b-instruct-fp16 --n_shots 2 --n_prototype 1 --include_guidelines
# LlamaCpp: python rb_script.py --backend llamacpp --root_dir src/renal_biopsy --model_name models/Phi-3.5-mini-instruct-Q5_K_M.gguf --n_shots 2 --n_prototype 1 --include_guidelines

if __name__ == "__main__":
    print("Ensure you have annotated some examples in the Streamlit app, saved it, and use that file here.")

    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", help="Model backend (ollama or llamacpp)", choices=['ollama', 'llamacpp'], required=True)
    parser.add_argument("--root_dir", help="Root directory for data modality", required=True, type=str)
    parser.add_argument("--model_name", help="LLM to use", required=True, type=str)
    parser.add_argument("--n_shots", help="Number of few-shot samples to use in prompt", default=2, type=int)
    parser.add_argument("--n_prototype", help="Number of samples to run (max is 2111)", default=1, type=int)
    parser.add_argument("--include_guidelines", help="Include entity guidelines in prompt?", action="store_true")
    args = parser.parse_args()

    if args.n_prototype > 2111:
        raise ValueError("n_prototype cannot exceed 2111.")

    # Check file existence
    root_dir = Path(args.root_dir)
    required_files = {
        "guidelines": root_dir / "data/guidelines.xlsx",
        "raw_data": root_dir / "data/full_data.xlsx",
        "annotated_reports": root_dir / "data/output_report_first100.json"
    }
    
    for file_path in required_files.values():
        if not file_path.exists():
            raise FileNotFoundError(f"Required file not found: {file_path}")

    # Create results directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = root_dir / "data" / "runs" / timestamp
    data_dir = results_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Copy input files to results directory
    for file_name, file_path in required_files.items():
        if file_path.suffix == '.xlsx':
            shutil.copy2(file_path, data_dir / file_path.name)

    # Initialise metadata
    metadata = {
        "args": vars(args),
        "annotation_start_time": None,
        "annotation_end_time": None,
        "evaluation_start_time": None,
        "evaluation_end_time": None,
        "score_per_report": None,
        "final_score": None
    }

    # Save initial metadata
    metadata_path = results_dir / "metadata.txt"
    write_metadata_file(metadata_path, metadata)

    try:
        # Create input JSON
        eg = EntityGuidelines(required_files["guidelines"])
        processor = RenalBiopsyProcessor(guidelines=eg)
        input_json = processor.create_input_json(
            data_path=required_files["raw_data"],
            save_path=root_dir / "data/real_input.json",
            full=True
        )
    except Exception as e:
        print(f"Error creating input JSON: {e}")
        raise

    try:
        # Load annotated JSON
        annotated_json = load_json(required_files["annotated_reports"])
        save_json(annotated_json, results_dir / "annotated.json")

        # Initialise appropriate model based on backend
        model_class = RenalBiopsyOllamaQA if args.backend == 'ollama' else RenalBiopsyLlamaCppQA
        model = model_class(model_path=args.model_name, root_dir=args.root_dir)
        
        # Run model
        metadata["annotation_start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract entities
        if args.backend == 'ollama':
            generated_answers = model.extract_with_known_entities(
                input_json, 
                n_shots=args.n_shots,
                n_prototype=args.n_prototype,
                include_guidelines=args.include_guidelines
            )
            save_json(generated_answers, results_dir / "generated_answers.json")
            
            predicted_json = model.convert_generated_answers_to_json(
                generated_answers=generated_answers,
                input_json=input_json,
                n_prototype=args.n_prototype
            )
        else:
            # LlamaCpp version returns predictions directly
            predicted_json = model.extract_with_known_entities(
                input_json,
                n_shots=args.n_shots,
                n_prototype=args.n_prototype,
                include_guidelines=args.include_guidelines
            )
        
        save_json(predicted_json, results_dir / "predicted.json")
        metadata["annotation_end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    except Exception as e:
        print(f"Error during model execution: {e}")
        raise

    try:
        # Evaluate predictions
        metadata["evaluation_start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        all_scores, score_per_report, final_score = model.evaluate(
            annotated_json,
            predicted_json,
            n_prototypes=args.n_prototype
        )
        entity_scores = model.calculate_entity_accuracy(all_scores)
        metadata["evaluation_end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save results
        save_json(all_scores, results_dir / "evaluation_scores.json")
        metadata["score_per_report"] = score_per_report
        metadata["final_score"] = final_score
        save_json(entity_scores, results_dir / "entity_scores.json")
        

    except Exception as e:
        print(f"Error during model evaluation: {e}")
        raise

    # Save final metadata
    write_metadata_file(metadata_path, metadata)
    print(f"Results saved to {results_dir}")