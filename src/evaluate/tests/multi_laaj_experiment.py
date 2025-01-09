import pandas as pd
import numpy as np
from typing import Dict, Callable
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
from .laaj_test_cases import comparison_cases_small, comparison_cases_medium, comparison_cases_large

class MultiLAAJExperiment:
    def __init__(self, llm_judges: Dict[str, Callable], n_trials: int = 5):
        """
        llm_judges: Dict mapping model names to their judge functions
        e.g. {
            'gemma': partial(use_llm_to_compare, model='gemma2:2b'),
            'llama': partial(use_llm_to_compare, model='llama2:7b'),
            'mistral': partial(use_llm_to_compare, model='mistral:7b')
        }
        """
        self.llm_judges = llm_judges
        self.n_trials = n_trials

    def load_test_cases(self) -> Dict:
        # return comparison_cases_medium
        return comparison_cases_large

    def run_trials(self) -> pd.DataFrame:
        results = []
        test_cases = self.load_test_cases()
        total_iterations = sum(len(pairs) * self.n_trials for pairs in test_cases.values())
        
        with tqdm(total=total_iterations, desc="Running trials") as pbar:
            for category, pairs in test_cases.items():
                for pair in pairs:
                    for trial in range(self.n_trials):
                        trial_results = {}
                        
                        # Get results from each model
                        for model_name, judge_fn in self.llm_judges.items():
                            result = judge_fn(pair[0], pair[1])
                            trial_results[model_name] = result
                        
                        # Calculate agreement between models
                        model_pairs = [(m1, m2) for i, m1 in enumerate(self.llm_judges.keys()) 
                                    for m2 in list(self.llm_judges.keys())[i+1:]]
                        
                        for m1, m2 in model_pairs:
                            agreement = trial_results[m1] == trial_results[m2]
                            
                            results.append({
                                'category': category,
                                'pair': f"{pair[0]} / {pair[1]}",
                                'trial': trial,
                                'model1': m1,
                                'model2': m2,
                                'agreement': agreement,
                                'result1': trial_results[m1],
                                'result2': trial_results[m2]
                            })
                        
                        pbar.update(1)
        
        return pd.DataFrame(results)

    def analyse_results(self, df: pd.DataFrame) -> Dict:
        metrics = {}
        
        # Calculate agreement rates between model pairs
        for category in df['category'].unique():
            category_df = df[df['category'] == category]
            
            model_pairs = category_df[['model1', 'model2']].drop_duplicates().values
            pair_metrics = {}
            
            for m1, m2 in model_pairs:
                pair_df = category_df[
                    (category_df['model1'] == m1) & 
                    (category_df['model2'] == m2)
                ]
                
                pair_metrics[f'{m1}_vs_{m2}'] = {
                    'agreement_rate': pair_df['agreement'].mean(),
                    'std_dev': pair_df['agreement'].std()
                }
            
            metrics[category] = pair_metrics
        
        return metrics

    def plot_results(self, metrics: Dict):
        # Prepare data for heatmap
        model_pairs = list(metrics['exact'].keys())
        categories = list(metrics.keys())
        
        agreement_matrix = np.zeros((len(categories), len(model_pairs)))
        
        for i, category in enumerate(categories):
            for j, model_pair in enumerate(model_pairs):
                agreement_matrix[i, j] = metrics[category][model_pair]['agreement_rate']
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(agreement_matrix, 
                   annot=True, 
                   fmt='.2f',
                   xticklabels=model_pairs,
                   yticklabels=categories,
                   cmap='YlOrRd')
        
        plt.title('Inter-Model Agreement Rates by Category')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return fig