import argparse
import tabula as tb
import pandas as pd
import json
import os
from PyPDF2 import PdfReader


def scrape_acronym_pdf(filename, page_num):
    """Scrape Acronym PDF.

    A function to scrape a pdf.

    Parameters
    ----------
    filename: str
        Name of PDF file
    page_num: int
        Integer representing page number

    Returns
    -------
    acronyms: pandas.core.series.Series
        Acronyms in a pandas series
    definitions: pandas.core.series.Series
        Definitions in a pandas series

    """
    data = tb.read_pdf(
        filename,
        area=(0, 0, 800, 800),
        columns=[0, 100, 800, 800],
        pages=str(page_num),
        pandas_options={"header": None},
        stream=True,
        lattice=True,
    )

    df = data[1]

    acronyms = df[0]
    definitions = df[2]
    return acronyms, definitions


def get_pdf_page_count(filename):
    """Get the number of pages in a PDF file.

    Parameters
    ----------
    filename: str
        Name of the PDF file

    Returns
    -------
    int
        Number of pages in the PDF file
    """
    with open(filename, "rb") as file:
        reader = PdfReader(file)
        return len(reader.pages)


def create_glossary(filename):
    """Create Glossary.

    A function to create a Glossary.

    Parameters
    ----------
    filename: str
        Name of PDF file
    """

    npages = get_pdf_page_count(filename)
    glossary = {}
    for i in range(1, npages + 1):
        acronym_series, definition_series = scrape_acronym_pdf(filename, i)
        for acronym, definition in zip(acronym_series, definition_series):
            if acronym in glossary:
                glossary[acronym] = glossary[acronym] + " | " + definition
            else:
                glossary[acronym] = definition

    pre, ext = os.path.splitext(filename)

    glossary_json = pre + ".json"
    with open(glossary_json, "w") as outfile:
        json.dump(glossary, outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create glossary from PDF.")
    parser.add_argument("filename", help="Name of the PDF file")
    args = parser.parse_args()

    create_glossary(args.filename)
