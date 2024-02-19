#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Original Code: Euclidator
Author: Yannick Copin
License: Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)
License URL: https://gitlab.euclid-sgs.uk/ycopin/euclidator/-/blob/master/LICENSE

Modified Code: Glossary
Author: Jennifer E. Pollack
License: MIT License
License URL: https://opensource.org/licenses/MIT

This script retrieves definitions for acronyms from a glossary stored in a JSON file.

Changes with respect to Original Code are:

Acronym List Removal
Removed the predefined list of acronyms (ecal) as it's no longer needed in the modified version.
The acronyms are now loaded from a JSON file using the `read_acronyms` function.

File Input for Acronyms
The `read_acronyms` function is responsible for loading acronyms and their definitions from a file.

JSON Dumping Removal
The `--json` argument which allows dumping the list of acronyms to a JSON file was removed.  The user
is expected to provide a json file containing the acronyms.

Refactored Acronym Retrieval
The logic for retrieving and printing acronym definitions has been refactored to work with the loaded acronyms dictionary.
The `read_acronyms` function is called to load acronyms from the file, and then the retrieval logic remains similar to the original code,
with adjustments to work with the loaded data.

"""

import argparse
from difflib import SequenceMatcher
import json


def get_similarity(a, b):
    """
    Calculate the similarity ratio between two strings using SequenceMatcher.

    Parameters
    ----------
    a: str
        First string.
    b: str
        Second string.

    Returns
    -------
    float
        Similarity ratio between the two strings.
    """
    return SequenceMatcher(None, a, b).ratio()


def parse_arguments():
    """
    Parse command-line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("acronym", nargs="*")
    parser.add_argument(
        "-g", "--glossary", type=str, help="JSON file storing acronym glossary"
    )
    parser.add_argument(
        "-E",
        "--regex",
        action="store_true",
        help="Interpret arguments as regular expressions.",
        default=False,
    )
    parser.add_argument(
        "-R",
        "--reversed",
        action="store_true",
        help="Reversed look-up (always regex).",
        default=False,
    )
    parser.add_argument(
        "-s",
        "--similarity",
        metavar="[0.0-1.0]",
        type=float,
        help="Print similar keywords, given a match fraction.",
        default=-1,
    )

    return parser.parse_args()


def load_glossary(file_path):
    """
    Load glossary from a JSON file.

    Parameters
    ----------
    file_path: str
        Path to the JSON file.

    Returns
    -------
    dict
        Loaded glossary

    Raises
    ------
        FileNotFoundError: If the glossary file is not found.
        ValueError: If the JSON file has invalid format.
    """
    try:
        with open(file_path, "r") as json_file:
            return json.loads(json_file.read())
    except FileNotFoundError:
        raise FileNotFoundError("Glossary JSON file not found.")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in glossary file.")


def retrieve_definitions(args, glossary):
    """
    Retrieve definitions for acronyms from the glossary.

    Parameters
    ----------
    args: argparse.Namespace
        Parsed command-line arguments.
    glossary: dict
        Dictionary containing acronyms and their definitions.

    Returns
    -------
    str
        Definition of the queried acronym.
    """
    nglossary = {k.lower(): v for k, v in glossary.items()}
    acronyms = args.acronym or sorted(glossary.keys())

    for acronym in acronyms:
        definition = nglossary.get(
            acronym.lower(), "Yet Another Unknown Acronym (YAUA)"
        )
        if 0 <= args.similarity <= 1:
            similars = [
                key
                for key in glossary
                if get_similarity(key, acronym) > args.similarity
            ]
            if similars:
                print("\nSimilar acronyms:", " ".join(similars), "\n")
        elif definition.endswith("(YAUA)"):
            similars = [
                key
                for key in glossary
                if get_similarity(key.lower(), acronym.lower()) > 0.7
            ]
            if similars:
                print("\nDid you mean:", " ".join(similars), "?\n")

    return definition


def main():
    """
    Main function to execute the acronym definition retrieval script.
    """
    args = parse_arguments()
    glossary = load_glossary(args.glossary)
    definition = retrieve_definitions(args, glossary)
    print(definition)
    return definition


if __name__ == "__main__":
    main()

# Local Variables:
# time-stamp-line-limit: 10
# End:
