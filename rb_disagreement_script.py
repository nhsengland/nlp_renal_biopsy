import argparse
import shutil
from datetime import datetime
from pathlib import Path

from src.preprocessing.guidelines import EntityGuidelines
from src.renal_biopsy.preprocessor import RenalBiopsyProcessor
from src.utils.json import save_json
from src.utils.general import write_metadata_file
from automated_annotation.disagreement import DisagreementAnnotator

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", help="Model backend (ollama or llamacpp)", choices=['ollama', 'llamacpp'], required=True)
    parser.add_argument("--root_dir", help="Root directory for data modality", required=True, type=str)
    parser.add_argument("--model_1_name", help="First LLM to use", required=True, type=str)
    parser.add_argument("--model_2_name", help="Second LLM to use", required=True, type=str)
    parser.add_argument("--n_shots", help="Number of few-shot samples to use in prompt", default=2, type=int)
    parser.add_argument("--n_prototype", help="Number of samples to run (max is 2111)", default=1, type=int)
    parser.add_argument("--disagreement_threshold", help="Threshold for clinician review", default=0.3, type=float)
    parser.add_argument("--include_guidelines", help="Include entity guidelines in prompt?", action="store_true")
    args = parser.parse_args()

    if args.n_prototype > 2111:
        raise ValueError("n_prototype cannot exceed 2111.")

    # Setup paths and check files
    root_dir = Path(args.root_dir)
    required_files = {
        "guidelines": root_dir / "data/guidelines.xlsx",
        "raw_data": root_dir / "data/full_data.xlsx",
        "annotated_reports": root_dir / "data/output_report_first100.json"
    }
    
    for file_path in required_files.values():
        if not file_path.exists():
            raise FileNotFoundError(f"Required file not found: {file_path}")

    # Create results directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = root_dir / "data" / "runs" / timestamp
    data_dir = results_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Copy input files
    for file_name, file_path in required_files.items():
        if file_path.suffix == '.xlsx':
            shutil.copy2(file_path, data_dir / file_path.name)

    # Initialise metadata
    metadata = {
        "args": vars(args),
        "total_annotation_start_time": None,
        "total_annotation_end_time": None,
        "disagreement_modelling_start_time": None,
        "disagreement_modelling_end_time": None,
        "reports_for_review": None,
        "n_reports_for_review": None
    }
    write_metadata_file(results_dir / "metadata.txt", metadata)

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
        # Create disagreement annotator
        da = DisagreementAnnotator(
            model_path_1=args.model_1_name,
            model_path_2=args.model_2_name,
            backend=args.backend,
            root_dir=str(root_dir)
        )

        metadata["total_annotation_start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Run model 1
        if args.backend == 'ollama':
            model_1_answers = da.model_1.extract_with_known_entities(
                input_json,
                n_shots=args.n_shots,
                n_prototype=args.n_prototype,
                include_guidelines=args.include_guidelines
            )
            save_json(model_1_answers, results_dir / "model_1_generated_answers.json")
            model_1_predicted = da.model_1.convert_generated_answers_to_json(
                generated_answers=model_1_answers,
                input_json=input_json,
                n_prototype=args.n_prototype
            )
        else:
            model_1_predicted = da.model_1.extract_with_known_entities(
                input_json,
                n_shots=args.n_shots,
                n_prototype=args.n_prototype,
                include_guidelines=args.include_guidelines
            )
            
        save_json(model_1_predicted, results_dir / "model_1_predicted.json")

        # Run model 2
        if args.backend == 'ollama':
            model_2_answers = da.model_2.extract_with_known_entities(
                input_json,
                n_shots=args.n_shots,
                n_prototype=args.n_prototype,
                include_guidelines=args.include_guidelines
            )
            save_json(model_2_answers, results_dir / "model_2_generated_answers.json")
            model_2_predicted = da.model_2.convert_generated_answers_to_json(
                generated_answers=model_2_answers,
                input_json=input_json,
                n_prototype=args.n_prototype
            )
        else:
            model_2_predicted = da.model_2.extract_with_known_entities(
                input_json,
                n_shots=args.n_shots,
                n_prototype=args.n_prototype,
                include_guidelines=args.include_guidelines
            )
            
        save_json(model_2_predicted, results_dir / "model_2_predicted.json")
        
        metadata["total_annotation_end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    except Exception as e:
        print(f"Error during model execution: {e}")
        raise

    try:
        # Analyse disagreements
        metadata["disagreement_modelling_start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entity_answers, report_counts, review_reports = da.analyse_disagreements(
            model_1_predicted,
            model_2_predicted,
            disagreement_threshold=args.disagreement_threshold,
            n_prototype=args.n_prototype
        )

        metadata["disagreement_modelling_end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save results
        save_json(entity_answers, results_dir / "entity_answers_over_corpus.json")
        save_json(report_counts, results_dir / "disagreement_counts.json")
        metadata["reports_for_review"] = review_reports
        metadata["n_reports_for_review"] = len(review_reports)

    except Exception as e:
        print(f"Error during disagreement analysis: {e}")
        raise

    # Save final metadata
    write_metadata_file(results_dir / "metadata.txt", metadata)
    print(f"Results saved to {results_dir}")