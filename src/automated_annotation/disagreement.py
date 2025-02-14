from typing import Dict, List, Tuple, Any
from pathlib import Path
from tqdm import tqdm

from src.renal_biopsy.preprocessor import RenalBiopsyProcessor
from renal_biopsy.qa import RenalBiopsyOllamaQA, RenalBiopsyLlamaCppQA
from preprocessing.guidelines import EntityGuidelines
from src.evaluate.laaj import use_llm_to_compare


class DisagreementAnnotator:
    """Analyses disagreements between two QA models' predictions on medical reports."""

    def __init__(
        self,
        model_path_1: str,
        model_path_2: str,
        backend: str,
        root_dir: str = "src/renal_biopsy",
    ):
        """
        Initialise with model paths, backend type, and root directory.

        Args:
            model_path_1: Path to first model
            model_path_2: Path to second model
            backend: Model backend ('ollama' or 'llamacpp')
            root_dir: Root directory containing data and models
        """
        if backend not in ["ollama", "llamacpp"]:
            raise ValueError("backend must be either 'ollama' or 'llamacpp'")

        self.root_dir = Path(root_dir)
        self.guidelines = EntityGuidelines(self.root_dir / "data/guidelines.xlsx")

        # Select appropriate model class
        model_class = (
            RenalBiopsyOllamaQA if backend == "ollama" else RenalBiopsyLlamaCppQA
        )

        # Initialise models
        self.model_1 = model_class(model_path=model_path_1, root_dir=root_dir)
        self.model_2 = model_class(model_path=model_path_2, root_dir=root_dir)

        # Store backend type for processing
        self.backend = backend

    def run_automated_annotation(
        self, n_shots: int = 3, n_prototype: int = 1, include_guidelines: bool = True
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Run automated annotation comparing predictions from both models.

        Args:
            n_shots: Number of examples for few-shot learning
            n_prototype: Number of prototypes to process
            include_guidelines: Whether to include guidelines in prompts

        Returns:
            Tuple of predictions from both models
        """
        # Process input data
        processor = RenalBiopsyProcessor(guidelines=self.guidelines)
        input_json = processor.create_input_json(
            data_path=self.root_dir / "data/full_data.xlsx",
            save_path=self.root_dir / "data/real_input.json",
            full=True,
        )

        # Get predictions from both models based on backend
        if self.backend == "ollama":
            predictions_1 = self._get_ollama_predictions(
                self.model_1, input_json, n_shots, n_prototype, include_guidelines
            )
            predictions_2 = self._get_ollama_predictions(
                self.model_2, input_json, n_shots, n_prototype, include_guidelines
            )
        else:
            predictions_1 = self._get_llamacpp_predictions(
                self.model_1, input_json, n_shots, n_prototype, include_guidelines
            )
            predictions_2 = self._get_llamacpp_predictions(
                self.model_2, input_json, n_shots, n_prototype, include_guidelines
            )

        return predictions_1, predictions_2

    def _get_ollama_predictions(
        self,
        model: RenalBiopsyOllamaQA,
        input_json: Dict[str, Any],
        n_shots: int,
        n_prototype: int,
        include_guidelines: bool,
    ) -> List[Dict[str, Any]]:
        """Get predictions from Ollama model."""
        answers = model.extract_with_known_entities(
            input_json,
            n_shots=n_shots,
            n_prototype=n_prototype,
            include_guidelines=include_guidelines,
        )
        return model.convert_generated_answers_to_json(answers, input_json, n_prototype)

    def _get_llamacpp_predictions(
        self,
        model: RenalBiopsyLlamaCppQA,
        input_json: Dict[str, Any],
        n_shots: int,
        n_prototype: int,
        include_guidelines: bool,
    ) -> List[Dict[str, Any]]:
        """Get predictions from LlamaCpp model."""
        return model.extract_with_known_entities(
            input_json,
            n_shots=n_shots,
            n_prototype=n_prototype,
            include_guidelines=include_guidelines,
        )

    def analyse_disagreements(
        self,
        predictions_1: List[Dict[str, Any]],
        predictions_2: List[Dict[str, Any]],
        disagreement_threshold: float = 0.3,
        n_prototype: int = 1,
    ) -> Tuple[List[Dict[str, bool]], List[Dict[str, int]], List[int]]:
        """Analyse disagreements between two sets of predictions."""
        entity_matches = []
        report_counts = []
        review_needed = []
        n_entities = len(self.guidelines.entity_to_info_map)

        for i, (pred1, pred2) in enumerate(
            tqdm(
                zip(predictions_1, predictions_2),
                total=n_prototype,
                desc="Analysing model disagreements",
                ncols=110,
            )
        ):
            if i == n_prototype:
                break

            matches, counts = self._compare_predictions(pred1, pred2)
            entity_matches.append(matches)
            report_counts.append(counts)

            if counts["mismatches"] / n_entities >= disagreement_threshold:
                review_needed.append(i)
                predictions_1[i]["clinician_check"] = True
                predictions_2[i]["clinician_check"] = True

        # Print summary
        self._print_disagreement_summary(report_counts, review_needed)

        return entity_matches, report_counts, review_needed

    def _compare_predictions(
        self, pred1: Dict[str, Any], pred2: Dict[str, Any]
    ) -> Tuple[Dict[str, bool], Dict[str, int]]:
        """Compare predictions for a single report."""
        entity_matches = {key: False for key in self.guidelines.entity_to_info_map}

        for entity, (_, entity_type, _) in self.guidelines.entity_to_info_map.items():
            value1 = pred1.get(entity)
            value2 = pred2.get(entity)

            if entity_type in ["boolean", "categorical", "numerical"]:
                entity_matches[entity] = value1 == value2
            else:
                entity_matches[entity] = use_llm_to_compare(
                    value1, value2, "gemma2:2b-instruct-fp16", "ollama"
                )

        counts = {
            "matches": sum(1 for v in entity_matches.values() if v),
            "mismatches": sum(1 for v in entity_matches.values() if not v),
        }

        return entity_matches, counts

    def _print_disagreement_summary(
        self, counts: List[Dict[str, int]], review_reports: List[int]
    ) -> None:
        """Print summary of disagreement analysis."""
        print(f"Reports requiring clinical review: {len(review_reports)}")
        for i, count in enumerate(counts):
            print(f"Report {i}: {count}")
