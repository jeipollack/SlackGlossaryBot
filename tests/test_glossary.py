"""UNIT TESTS FOR MODULE: Glossary.

This module contains unit tests for the glossary module.

:Author: Jennifer Pollack <jennifer.pollack@cea.fr>

"""

from pathlib import Path
import pytest
from SlackGlossaryBot.glossary import glossary
import json


@pytest.fixture
def mock_glossary_json_data(tmp_path: Path):
    glossary_data = [
        {
            "Term": "NASA",
            "Description": "National Aeronautics and Space Administration",
        },
        {"Term": "NASA", "Description": "North American Saxophone Alliance"},
        {
            "Term": "ATLAS",
            "Description": "Advanced Technology Large-Aperture Space Telescope",
        },
        {
            "Term": "ATLAS",
            "Description": "Automated Teaching and Learning Assessment System",
        },
    ]
    file_path = tmp_path / "temp_glossary.json"
    with open(file_path, "w") as f:
        json.dump(glossary_data, f)
    return str(file_path)


@pytest.fixture
def mock_glossary_csv_data(tmp_path: Path):
    # Define the CSV data
    glossary_data = """\
    Term,Description,Subsystem Tags,Documentation Tags,Associated Acronyms and Alternative Terms,Type
    BPS,Batch Production Service,DF LDF DM,,,A
    Bps,Bytes per second,Gen,,,A
    bps,bit(s) per second,Gen,,,A   
    """
    # Create a temporary file path
    csv_file_path = tmp_path / "mock_glossary.csv"

    # Write the CSV data to the temporary file
    with open(csv_file_path, "w") as f:
        f.write(glossary_data)

    # Yield the path to the temporary file
    yield csv_file_path


def test_load_json_glossary_concatenation(mock_glossary_json_data: str):
    glossary_data = glossary.load_glossary(
        {"path": mock_glossary_json_data, "file_type": "json"}
    )
    assert glossary_data["nasa"] == [
        "National Aeronautics and Space Administration",
        "North American Saxophone Alliance",
    ]
    assert glossary_data["atlas"] == [
        "Advanced Technology Large-Aperture Space Telescope",
        "Automated Teaching and Learning Assessment System",
    ]


def test_load_csv_glossary_concatenation(mock_glossary_csv_data: str):
    glossary_data = glossary.load_glossary(
        {"path": mock_glossary_csv_data, "file_type": "csv"}
    )

    assert glossary_data["bps"] == [
        "Batch Production Service",
        "Bytes per second",
        "bit(s) per second",
    ]
