import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict
from tqdm import tqdm

from .laaj_test_cases import (
    comparison_cases_small,
    comparison_cases_medium,
    comparison_cases_large,
)

ccs = {
    "small": comparison_cases_small,
    "medium": comparison_cases_medium,
    "large": comparison_cases_large,
}


def test_symmetry(pairs, llm_compare_fn):
    """Test if comparisons are symmetric (does A with B give same as B with A)."""
    symmetry_results = []
    for e1, e2 in pairs:
        forward = llm_compare_fn(e1, e2)
        backward = llm_compare_fn(e2, e1)
        symmetry_results.append(forward == backward)
    return sum(symmetry_results) / len(symmetry_results)


def test_consistency(pairs, llm_compare_fn, n_trials=5):
    """Test consistency of comparisons across multiple runs."""
    consistency_results = []
    for e1, e2 in pairs:
        trial_results = []
        for _ in range(n_trials):
            trial_results.append(llm_compare_fn(e1, e2))
        # Calculate consistency as ratio of most common result
        consistency = (
            max(trial_results.count(True), trial_results.count(False)) / n_trials
        )
        consistency_results.append(consistency)
    return sum(consistency_results) / len(consistency_results)


class LAAJExperiment:
    def __init__(
        self, llm_judge_fn, comparison_case_set_size: str = "small", n_trials: int = 1
    ):
        self.llm_judge_fn = llm_judge_fn
        self.comparison_cases = ccs[comparison_case_set_size]
        self.n_trials = n_trials

    def load_test_cases(self) -> Dict:
        # In practice, load from a JSON file
        return self.comparison_cases

    def create_expert_annotations_from_comparison_cases(self, comparison_cases) -> Dict:
        # In practice, load from a JSON file
        expert_annotations = {}

        # Exact matches should be True
        for pair in comparison_cases["exact"]:
            expert_annotations[pair] = True

        # Same concepts should be True
        for pair in comparison_cases["same_concept"]:
            expert_annotations[pair] = True

        # Similar cases should be True
        for pair in comparison_cases["similar_enough"]:
            expert_annotations[pair] = True

        # Different cases should be False
        for pair in comparison_cases["different"]:
            expert_annotations[pair] = False

        return expert_annotations

    def run_trials(self) -> pd.DataFrame:
        results = []
        test_cases = self.load_test_cases()
        expert_annotations = self.create_expert_annotations_from_comparison_cases(
            test_cases
        )

        total_iterations = sum(
            len(pairs) * self.n_trials for pairs in test_cases.values()
        )

        with tqdm(total=total_iterations, desc="Running trials") as pbar:
            for category, pairs in test_cases.items():
                for pair in pairs:
                    expert_label = expert_annotations[pair]

                    for trial in range(self.n_trials):
                        forward = self.llm_judge_fn(pair[0], pair[1])
                        backward = self.llm_judge_fn(pair[1], pair[0])

                        results.append(
                            {
                                "category": category,
                                "pair": f"{pair[0]} / {pair[1]}",
                                "trial_number": trial,
                                "forward_result": forward,
                                "backward_result": backward,
                                "symmetric": forward == backward,
                                "expert_agreement": forward == expert_label,
                                "consistent_with_expert": forward == expert_label
                                and backward == expert_label,
                            }
                        )
                        pbar.update(1)

        return pd.DataFrame(results)

    def analyse_results(self, df: pd.DataFrame) -> Dict:
        metrics = {}

        for category in df["category"].unique():
            category_df = df[df["category"] == category]

            metrics[category] = {
                "symmetry": category_df["symmetric"].mean(),
                "expert_agreement": category_df["expert_agreement"].mean(),
                "consistency": category_df["consistent_with_expert"].mean(),
                "std_dev": category_df["expert_agreement"].std(),
            }

        return metrics

    def plot_results(self, metrics: Dict, results_df: pd.DataFrame):
        categories = list(metrics.keys())
        symmetry_scores = [m["symmetry"] for m in metrics.values()]
        agreement_scores = [m["expert_agreement"] for m in metrics.values()]
        consistency_scores = [m["consistency"] for m in metrics.values()]
        std_devs = [m["std_dev"] for m in metrics.values()]

        # Count number of unique pairs per category
        category_counts = results_df.groupby("category")["pair"].nunique()

        fig, ax = plt.subplots(figsize=(10, 6))

        x = np.arange(len(categories))
        width = 0.25

        ax.bar(x - width, symmetry_scores, width, label="Symmetry", color="skyblue")
        ax.bar(x, agreement_scores, width, label="Expert Agreement", color="lightgreen")
        ax.bar(
            x + width, consistency_scores, width, label="Consistency", color="salmon"
        )

        # Add error bars
        ax.errorbar(
            x, agreement_scores, yerr=std_devs, fmt="none", color="black", capsize=5
        )

        ax.set_ylabel("Score")
        ax.set_title("LLM Judge Performance Across Term Relationships")
        ax.set_xticks(x)
        ax.set_xticklabels(
            [f"{cat}\n(n={category_counts[cat]})" for cat in categories], rotation=45
        )
        ax.legend()

        # Set y-axis limits from 0 to 1
        ax.set_ylim(0, 1)

        plt.tight_layout()
        return fig
