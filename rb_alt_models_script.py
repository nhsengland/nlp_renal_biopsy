import argparse
import os
from typing import Tuple
import time

from src.utils.json import load_json, convert_to_strings, save_json
from src.preprocessing.guidelines import EntityGuidelines
from src.evaluate.alt_models import evaluate, calculate_entity_accuracy
from src.renal_biopsy.preprocessor import RenalBiopsyProcessor
from src.renal_biopsy.alt_models.spacy import process_reports
from src.renal_biopsy.alt_models.bert_qa import run_bertqa
from src.renal_biopsy.alt_models.gliner import (
    transform_gliner_annotations,
    gliner_label_mapping,
)
from gliner import GLiNER


def run_spacy_model(input_json: dict, output_path: str) -> Tuple[dict, float]:
    """Run and evaluate SpaCy model."""
    print("\nProcessing SpaCy model...")
    start_time = time.time()
    results, docs = process_reports(input_json, n_prototype=100)
    processing_time = (time.time() - start_time) / 60
    print(f"SpaCy processing time: {processing_time:.2f} minutes")

    save_json(results, f"{output_path}/spacy_first100.json")
    return results, processing_time


def run_biobert_model(input_json: dict, output_path: str) -> Tuple[dict, float]:
    """Run and save results for BioBERT model."""
    print("\nProcessing BioBERT model...")
    start_time = time.time()
    bb_results = run_bertqa(input_json[:100], "dmis-lab/biobert-large-cased-v1.1-squad")
    print(f"BioBERT processing time: {(time.time() - start_time)/60:.2f} minutes")
    save_json(bb_results, f"{output_path}/biobert_squad_first100.json")
    return bb_results, (time.time() - start_time) / 60


def run_roberta_model(input_json: dict, output_path: str) -> Tuple[dict, float]:
    """Run and save results for RoBERTa model."""
    print("\nProcessing RoBERTa model...")
    start_time = time.time()
    rb_results = run_bertqa(input_json[:100], "deepset/roberta-base-squad2")
    print(f"RoBERTa processing time: {(time.time() - start_time)/60:.2f} minutes")
    save_json(rb_results, f"{output_path}/roberta_squad_first100.json")
    return rb_results, (time.time() - start_time) / 60


def run_gliner_model(
    input_json: dict,
    output_path: str,
    model_name: str = "urchade/gliner_large_bio-v0.1",
) -> Tuple[dict, float]:
    """Run and evaluate GLiNER model."""
    print("\nProcessing GLiNER model...")
    model = GLiNER.from_pretrained(model_name)
    model.eval()

    n_to_annotate = 100
    gliner_annotated_reports = []
    threshold = 0.3  # NOTE: we optimised for this but can change

    start_time = time.time()
    for i, json_report in enumerate(input_json):
        if i == n_to_annotate:
            break
        annotated_report = model.predict_entities(
            json_report, list(gliner_label_mapping.keys()), threshold=threshold
        )
        gliner_annotated_reports.append(annotated_report)

    print(f"GLiNER processing time: {(time.time() - start_time)/60:.2f} minutes")

    final_reports, processed_reports = transform_gliner_annotations(
        gliner_annotated_reports, gliner_label_mapping
    )

    save_json(final_reports, f"{output_path}/gliner_first100_03_raw.json")
    save_json(processed_reports, f"{output_path}/gliner_first100_03_processed.json")

    processing_time = (time.time() - start_time) / 60
    return processed_reports, processing_time


def evaluate_model(
    qa_gt_json: dict, model_results: dict, eg: EntityGuidelines, model_name: str
):
    """Evaluate a single model and print results."""
    print(f"\nEvaluating {model_name}...")
    all_scores, scores_per_report, final_score = evaluate(
        qa_gt_json, model_results, eg, 100
    )
    entity_scores = calculate_entity_accuracy(all_scores, eg)

    print(f"{model_name} final score: {final_score}")
    # print(f"{model_name} entity scores:")
    # for entity, score in entity_scores.items():
    #    print(f"  {entity}: {score}")

    return final_score, entity_scores


def convert_input_to_text(input_json):
    final_input = []
    for report_dict in input_json:
        report_text = f"""MICROSCOPY SECTION: {report_dict['microscopy_section']}
                        CONCLUSION SECTION: {report_dict['conclusion_section']}"""
        final_input.append(report_text)
    return final_input


def load_input_data(root_dir: str, data_file: str, annotated_file: str):
    """Load all required input data."""
    # Create input JSON
    eg = EntityGuidelines(f"{root_dir}/guidelines.xlsx")
    processor = RenalBiopsyProcessor(guidelines=eg)
    input_json = processor.create_input_json(
        data_path=f"{root_dir}/{data_file}",
        save_path=None,
        full=True,
    )
    final_input = convert_input_to_text(input_json)
    qa_gt_json = load_json(f"{root_dir}/{annotated_file}")
    return final_input, qa_gt_json, eg


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Run and evaluate NLP models")

    parser.add_argument(
        "--root_dir",
        help="Path to data files",
        default="src/renal_biopsy/data",
        type=str,
    )
    parser.add_argument(
        "--data_file",
        help="Name of raw data file",
        default="full_data.xlsx",
        type=str,
    )
    parser.add_argument(
        "--annotated_reports_file",
        help="Name of annotated reports file",
        default="annotations.json",
        type=str,
    )
    parser.add_argument(
        "--output_dir",
        help="Directory for output files",
        default="src/renal_biopsy/data/runs/alt_models",
        type=str,
    )

    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Load input data
    input_json, qa_gt_json, eg = load_input_data(
        args.root_dir, args.data_file, args.annotated_reports_file
    )

    # Run all models and track times
    spacy_results, spacy_time = run_spacy_model(input_json, args.output_dir)
    biobert_results, biobert_time = run_biobert_model(input_json, args.output_dir)
    roberta_results, roberta_time = run_roberta_model(input_json, args.output_dir)
    gliner_results, gliner_time = run_gliner_model(input_json, args.output_dir)

    # Store results and times
    models = {
        "spaCy": {"results": convert_to_strings(spacy_results), "time": spacy_time},
        "BioBERT": {
            "results": convert_to_strings(biobert_results),
            "time": biobert_time,
        },
        "RoBERTa": {
            "results": convert_to_strings(roberta_results),
            "time": roberta_time,
        },
        "GLiNER": {"results": convert_to_strings(gliner_results), "time": gliner_time},
    }

    final_scores = {}
    all_entity_scores = {}

    processing_times = {}
    for model_name, model_data in models.items():
        final_score, entity_scores = evaluate_model(
            qa_gt_json, model_data["results"], eg, model_name
        )
        final_scores[model_name] = final_score
        all_entity_scores[model_name] = entity_scores
        processing_times[model_name] = model_data["time"]

    # Save evaluation results
    evaluation_results = {
        "final_scores": final_scores,
        "entity_scores": all_entity_scores,
        "processing_times": processing_times,
    }
    save_json(evaluation_results, f"{args.output_dir}/evaluation_results.json")

    # Print comprehensive comparison
    print("\nFinal Model Comparison:")
    for model_name in final_scores:
        print(f"{model_name}:")
        print(f"  Score: {final_scores[model_name]:.3f}")
        print(f"  Processing time: {processing_times[model_name]:.2f} minutes")


if __name__ == "__main__":
    main()
