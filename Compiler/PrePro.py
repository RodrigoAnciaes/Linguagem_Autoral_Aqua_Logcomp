"""

Preprocessor module for the Lua compiler.

This module contains the PrePro class, which is used to preprocess a string before parsing it.

Example:
    string = PrePro.filter(string)

This will remove all Lua comments from the string.

"""


import re


class PrePro:
    """
    Class to preprocess a string before parsing it.

    Attributes:
        None

    Methods:
        filter(string): Remove all Lua comments from a string.

    """
    @staticmethod
    def filter(string):
        """
        Remove all Lua comments from a string.

        Args:
            string (str): The input string.

        Returns:
            str: The string with Lua comments removed.
        """
        # Split the string by lines
        lines = string.split("\n")
        # Iterate over the lines using enumerate
        for i, line in enumerate(lines):
            # Remove Lua comments
            lines[i] = re.sub(r"--.*", "", line)
        # Remove empty lines from the list
        lines = list(filter(None, lines))
        # Join the lines back into a single string
        return "\n".join(lines)
