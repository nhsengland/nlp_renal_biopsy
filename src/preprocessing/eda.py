import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from collections import defaultdict
from typing import List, Dict, Optional, Union, Any
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import spacy
from gensim import corpora


class MedicalReportEDA:
    """
    Class for performing exploratory data analysis on medical report text.
    
    Provides functionality for analysing and visualising medical report text data,
    including word frequencies, section lengths, and text statistics.
    """
    
    def __init__(self, spacy_model: str = "en_core_web_sm"):
        """
        Initialise the EDA class.
        
        Args:
            spacy_model: Name of spaCy model to use for text processing
        """
        self.nlp = spacy.load(spacy_model)
        self.stop_words = set(self.nlp.Defaults.stop_words)
    
    def analyse_word_distributions(
        self,
        sections: List[str],
        label: str = 'Section',
        figsize: tuple = (12, 6)
    ) -> None:
        """
        Plot word and character count distributions for text sections.
        
        Args:
            sections: List of text sections to analyse
            label: Label for the plot titles
            figsize: Figure size for the plots
        """
        word_counts = [len(section.strip().split()) for section in sections]
        char_counts = [len(section) for section in sections]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Word count histogram
        ax1.hist(word_counts, bins=range(0, max(word_counts) + 10, 5),
                alpha=0.7, edgecolor='black')
        ax1.set_title(f'Word Count Distribution per {label}')
        ax1.set_xlabel('Number of Words')
        ax1.set_ylabel('Frequency')
        ax1.grid(axis='y')
        
        # Character count histogram
        ax2.hist(char_counts, bins=range(0, max(char_counts) + 10, 10),
                alpha=0.7, edgecolor='black')
        ax2.set_title(f'Character Count Distribution per {label}')
        ax2.set_xlabel('Number of Characters')
        ax2.set_ylabel('Frequency')
        ax2.grid(axis='y')
        
        plt.tight_layout()
        plt.show()
    
    def analyse_section_lengths(
        self,
        reports: List[Dict[str, str]],
        exclude_keys: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Analyse and visualise lengths of different sections in reports.
        
        Args:
            reports: List of report dictionaries
            exclude_keys: Keys to exclude from analysis
            
        Returns:
            DataFrame with length statistics
        """
        exclude_keys = exclude_keys or []
        lengths = []
        
        for report in reports:
            report_lengths = {
                section: len(str(text)) if text and not isinstance(text, int) else 0
                for section, text in report.items()
                if section not in exclude_keys
            }
            lengths.append(report_lengths)
        
        lengths_df = pd.DataFrame(lengths)
        stats = lengths_df.describe()
        
        plt.figure(figsize=(10, 6))
        lengths_df.plot(kind='box')
        plt.title(f'Section Length Distribution (n={len(reports)})')
        plt.ylabel('Characters')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        return stats
    
    def analyse_word_frequencies(
        self,
        section: List[str],
        n_terms: int = 40,
        figsize: tuple = (10, 6)
    ) -> pd.DataFrame:
        """
        Analyse and visualise word frequencies using CountVectorizer.
        
        Args:
            sections: List of text sections
            n_terms: Number of top terms to display
            figsize: Figure size for the plot
            
        Returns:
            DataFrame with term frequencies
        """
        vectoriser = CountVectorizer()
        count_matrix = vectoriser.fit_transform(sections)
        terms = vectoriser.get_feature_names_out()
        term_counts = count_matrix.toarray().sum(axis=0)
        
        freq_df = pd.DataFrame(term_counts, index=terms, columns=["Count"])
        freq_df = freq_df.sort_values(by="Count", ascending=False)
        
        plt.figure(figsize=figsize)
        sns.barplot(x=freq_df.index[:n_terms], y=freq_df['Count'][:n_terms],
                   palette='viridis')
        plt.title('Word Frequency Distribution')
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        return freq_df
    
    def analyse_word_frequencies_spacy(
        self,
        reports: List[Dict[str, str]],
        section_key: str,
        highlight_words: List[str],
        n_terms: int = 40
    ) -> pd.DataFrame:
        """
        Analyse word frequencies using spaCy processing.
        
        Args:
            reports: List of report dictionaries
            section_key: Key for the section to analyse
            highlight_words: Words to highlight in visualisation
            n_terms: Number of top terms to display
            
        Returns:
            DataFrame with word frequencies
        """
        texts = [report[section_key] for report in reports if report.get(section_key)]
        
        processed_texts = [
            [token.text for token in self.nlp(text.lower())
             if token.is_alpha and token.text not in self.stop_words]
            for text in texts
        ]
        
        dictionary = corpora.Dictionary(processed_texts)
        word_freq = dictionary.doc2bow(sum(processed_texts, []))
        
        freq_df = pd.DataFrame(word_freq, columns=['Word ID', 'Frequency'])
        freq_df['Word'] = freq_df['Word ID'].apply(lambda x: dictionary[x])
        freq_df = freq_df.sort_values(by='Frequency', ascending=False)
        freq_df['Highlight'] = freq_df['Word'].isin(highlight_words)
        
        # Visualisation
        plt.figure(figsize=(10, 6))
        colors = ['orange' if x else 'blue' for x in freq_df['Highlight']]
        sns.barplot(x='Frequency', y='Word', data=freq_df.head(n_terms),
                   palette=colors)
        
        plt.title(f'Top {n_terms} Words in {section_key} Sections')
        plt.xlabel('Frequency')
        plt.ylabel('Words')
        
        handles = [
            plt.Line2D([0], [0], color='orange', lw=4, label='Highlighted'),
            plt.Line2D([0], [0], color='blue', lw=4, label='Other'),
        ]
        plt.legend(handles=handles, title="Word Type")
        plt.tight_layout()
        plt.show()
        
        return freq_df
    
    def analyse_tfidf(
        self,
        sections: List[str],
        n_terms: int = 30,
        custom_stop_words: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Analyse and visualise TF-IDF scores across documents.
        
        Args:
            sections: List of text sections
            n_terms: Number of terms to include
            custom_stop_words: Additional stop words to exclude
            
        Returns:
            DataFrame with TF-IDF scores
        """
        stop_words = custom_stop_words or [
            'and', 'are', 'but', 'in', 'is', 'no', 'of', 'the',
            'there', 'with', 'seen', 'show', 'shows', 'to', 'which'
        ]
        
        vectoriser = TfidfVectorizer(max_features=n_terms, stop_words=stop_words)
        tfidf_matrix = vectoriser.fit_transform(sections)
        
        tfidf_df = pd.DataFrame(
            tfidf_matrix.toarray(),
            columns=vectoriser.get_feature_names_out(),
            index=[f'Doc {i+1}' for i in range(len(sections))]
        )
        
        plt.figure(figsize=(15, 20))
        sns.heatmap(tfidf_df, cmap='YlGnBu', annot=True, fmt=".2f",
                   linewidths=.5)
        plt.title(f'TF-IDF Heatmap (Top {n_terms} Terms)')
        plt.xlabel('Terms')
        plt.ylabel('Documents')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        return tfidf_df
        
    def calculate_report_statistics(
        self,
        reports: List[Dict[str, str]],
        section_keys: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculate comprehensive statistics for report sections.
        
        Args:
            reports: List of report dictionaries
            section_keys: Optional list of section keys to analyse. If None, uses all keys
                       from the first report.
                       
        Returns:
            Dictionary containing statistics for each section and combined metrics:
            - Min, max, average, and standard deviation lengths
            - Number of empty/None sections
            
        Raises:
            ValueError: If reports list is empty
        """
        if not reports:
            raise ValueError("Report list cannot be empty")
        
        # Use all keys from first report if none specified
        section_keys = section_keys or list(reports[0].keys())
        
        # Initialise length tracking
        section_lengths = defaultdict(list)
        total_lengths = []
        
        # Calculate lengths for each report
        for report in reports:
            report_total_length = 0
            
            for key in section_keys:
                if key in report:
                    section_text = report[key] if report[key] is not None else ""
                    length = len(str(section_text))
                    section_lengths[key].append(length)
                    report_total_length += length
                else:
                    print(f"Warning: Section '{key}' not found in report")
                    section_lengths[key].append(0)
            
            total_lengths.append(report_total_length)
        
        # Calculate statistics
        stats = {
            'sections': {
                key: {
                    'min': min(section_lengths[key]),
                    'max': max(section_lengths[key]),
                    'average': np.mean(section_lengths[key]),
                    'std_dev': np.std(section_lengths[key]),
                    'n_empty': sum(1 for length in section_lengths[key] if length == 0)
                }
                for key in section_keys
            },
            'combined': {
                'min': min(total_lengths),
                'max': max(total_lengths),
                'average': np.mean(total_lengths),
                'std_dev': np.std(total_lengths)
            }
        }
        
        # Print formatted results
        for section, metrics in stats['sections'].items():
            print(f"\n{section}:")
            print(f"  Min length: {metrics['min']}")
            print(f"  Max length: {metrics['max']}")
            print(f"  Average length: {metrics['average']:.2f}")
            print(f"  Standard deviation: {metrics['std_dev']:.2f}")
            print(f"  Number of empty/None sections: {metrics['n_empty']}")

        print("\nCombined Report:")
        print(f"  Min length: {stats['combined']['min']}")
        print(f"  Max length: {stats['combined']['max']}")
        print(f"  Average length: {stats['combined']['average']:.2f}")
        print(f"  Standard deviation: {stats['combined']['std_dev']:.2f}")
        
        return stats