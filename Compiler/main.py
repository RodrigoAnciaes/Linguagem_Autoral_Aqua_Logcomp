"""
Module: main
Description: This script processes a file through preprocessing and parsing steps,
             ultimately evaluating the parsed data.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from Compiler.prsr import Prsr
from Compiler.pre_pro import PrePro


def main():
    """
    Main function to process a file. It reads the file, applies preprocessing,
    parses the content, and evaluates the resulting abstract syntax tree.

    Usage:
        python main.py <filename>

    Args:
        None, but expects a filename as a command-line argument.

    Returns:
        None
    """
    arquive = sys.argv[1]
    with open(arquive, 'r', encoding='utf-8') as file:
        string = file.read()
    string = PrePro.filter(string)
    abstract_sintact_tree = Prsr.run(string)
    if abstract_sintact_tree:  # Ensure evaluate() is only called if the result is not None
        abstract_sintact_tree.evaluate()

if __name__ == "__main__":
    main()
