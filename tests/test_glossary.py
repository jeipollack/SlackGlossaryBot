"""UNIT TESTS FOR MODULE: Glossary.

This module contains unit tests for the glossary module.

:Author: Jennifer Pollack <jennifer.pollack@cea.fr>

"""

import pytest
from SlackGlossaryBot.glossary import glossary
import json


@pytest.fixture
def mock_glossary_data(tmp_path):
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


def test_load_glossary_concatenation(mock_glossary_data):
    glossary_data = glossary.load_glossary(
        {"path": mock_glossary_data, "file_type": "json"}
    )
    assert glossary_data["nasa"] == [
        "National Aeronautics and Space Administration",
        "North American Saxophone Alliance",
    ]
    assert glossary_data["atlas"] == [
        "Advanced Technology Large-Aperture Space Telescope",
        "Automated Teaching and Learning Assessment System",
    ]
