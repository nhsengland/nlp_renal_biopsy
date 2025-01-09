"""
Text processing utility functions for handling long text content and metadata.
Provides functionality for text wrapping, line insertion, and metadata writing.
"""

import textwrap
from typing import Optional, Dict, Any
from pathlib import Path


def wrap_text(text: str, max_length: int = 100) -> str:
    """
    Wrap text to a specified maximum line length while preserving existing newlines.
    
    Args:
        text: Input text to wrap
        max_length: Maximum length for each line
        
    Returns:
        Text with lines wrapped to specified length
        
    Example:
        >>> long_text = "This is a very long line that needs wrapping..."
        >>> print(wrap_text(long_text, max_length=40))
        This is a very long line that needs
        wrapping...
    """
    lines = text.split('\n')
    wrapped_lines = [textwrap.fill(line, width=max_length) for line in lines]
    return '\n'.join(wrapped_lines)


def insert_newlines(text: Optional[str], interval: int = 80) -> Optional[str]:
    """
    Insert newlines into text at regular intervals.
    
    Args:
        text: Input text to process
        interval: Number of characters between newlines
        
    Returns:
        Text with newlines inserted or None if input is None
        
    Example:
        >>> text = "A long string without any breaks"
        >>> print(insert_newlines(text, interval=10))
        A long str
        ing withou
        t any brea
        ks
    """
    if text is None:
        return None
    return '\n'.join(text[i:i+interval] for i in range(0, len(text), interval))


def write_metadata_file(metadata_path: str | Path, metadata: Dict[str, Any]) -> None:
    """
    Write metadata dictionary to a text file.
    
    Args:
        metadata_path: Path to output file
        metadata: Dictionary of metadata to write
    """
    with open(metadata_path, "w", encoding="utf-8") as f:
        for key, value in metadata.items():
            f.write(f"{key}: {value}\n")