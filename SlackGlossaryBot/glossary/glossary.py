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
import yaml
import pandas as pd
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
        "-c",
        "--config_file",
        type=str,
        help="YAML file storing configuration options.",
        default="config.yml",
    )

    return parser.parse_args()


def load_config(file_path):
    """
    Load configuration from a YAML file.

    Parameters
    ----------
    file_path: str
        Path to the YAML file.

    Returns
    -------
    dict
        Loaded configuration options.

    Raises
    ------
        FileNotFoundError: If the config file is not found.
        yaml.YAMLError: If the YAML file has invalid format.
    """
    try:
        with open(file_path, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
    except FileNotFoundError:
        raise FileNotFoundError("Config YAML file not found.")
    except yaml.YAMLError:
        raise ValueError("Invalid YAML format in config file.")


def load_glossary(config):
    """
    Load glossary from a JSON file.

    Parameters
    ----------
    config: dict
        Dictionary containing configuration options.

    Returns
    -------
    dict
        Loaded glossary

    Raises
    ------
        FileNotFoundError: If the glossary file is not found.
        ValueError: If the JSON file has invalid format.
    """
    glossary_file = config["path"]
    glossary_type = config["file_type"]

    # Load glossary based on the file type
    if glossary_type.lower() == "json":
        with open(glossary_file, "r") as f:
            glossary = json.load(f)
    elif glossary_type.lower() == "csv":
        # Load glossary from CSV file
        glossary_df = pd.read_csv(glossary_file)
        # Group the DataFrame by 'Term' (acronym) and aggregate the descriptions into a list
        glossary_grouped = glossary_df.groupby("Term")["Description"].agg(list)
        # Convert the grouped DataFrame to a dictionary
        glossary = glossary_grouped.to_dict()
    else:
        raise ValueError("Unsupported file type:", glossary_type)
    return glossary


def retrieve_definitions(args, glossary, language_phrases, similarity=1):
    """
    Retrieve definitions for acronyms from the glossary.

    Parameters
    ----------
    args: argparse.Namespace
        Parsed command-line arguments.
    glossary: dict
        Dictionary containing acronyms and their definitions.
    language_phrases: dict
        Dictionary containing language phrases in the Bot response.
    similarity: int
        Similarity ratio between the two strings.

    Returns
    -------
    str
        Definition of the queried acronym.
    """
    nglossary = {k.lower(): v for k, v in glossary.items()}
    acronyms = args.acronym or sorted(glossary.keys())

    for acronym in acronyms:
        definition = nglossary.get(
            acronym.lower(), [language_phrases["acronym_not_found"]]
        )

        if language_phrases["acronym_not_found"] in definition:
            similars = [
                key
                for key in glossary
                if get_similarity(key.lower(), acronym.lower()) > 0.7
            ]

            if similars:
                print(language_phrases["helper"], " ".join(similars), "?\n")

    return " | ".join(definition)


def main():
    """
    Main function to execute the acronym definition retrieval script.
    """
    args = parse_arguments()
    config = load_config(args.config_file)
    # Select language-specific phrases based on configuration
    language = config.get(
        "language", "english"
    )  # Default to English if language is not specified
    language_phrases = {
        "english": {
            "acronym_not_found": "Acronym Unknown (AU)",
            "helper": "\nDid you mean:",
        },
        "spanish": {
            "acronym_not_found": "Acrónimo Desconocido (AD)",
            "helper": "\n¿Querías decir:",
        },
    }.get(
        language,
        {
            "acronym_not_found": "Acronym Unknown (AU)",
            "helper": "\nDid you mean:",
        },
    )
    glossary = load_glossary(config)
    definition = retrieve_definitions(
        args, glossary, language_phrases, config["similarity"]
    )
    print(definition)
    return definition


if __name__ == "__main__":
    main()

# Local Variables:
# time-stamp-line-limit: 10
# End:
