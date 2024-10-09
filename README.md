## MBI-KG: A knowledge graph of structured and linked economic research data extracted from the book "Die Maschinen-Industrie im Deutschen Reich" written by Herbert Patschan in 1937

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/shigapov/ReproResearch/blob/main/CODE_OF_CONDUCT.md) 
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Open Code](https://badgen.net/static/open/code/green)](https://github.com/UB-Mannheim/MBI-KG/tree/main/code)
[![Open Data](https://badgen.net/static/open/data/green)](https://github.com/UB-Mannheim/MBI-KG/tree/main/data)
[![Open Science](https://badgen.net/static/open/science/green)](https://en.wikipedia.org/wiki/Open_science)

### Table of contents

* [Repo structure](#repo-structure)
  * [Docs](#docs)
  * [Data](#data)
  * [Code](#code)
* [How to contribute](#how-to-contribute)
* [License](#license)

### Repo structure

```
MBI-KG/
├── docs/
│   ├── talks/
│   ├── sparql_examples/
│   └── README_docs.md
├── data/
│   ├── structured_data/
│   ├── scanned_images/
│   ├── ocr_output/
│   ├── models/
│   └── README_data.md
├── code/
│   ├── requirements.txt
│   ├── book2entities.py
│   └── README_code.md
├── README.md
├── LICENSE.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── CITATION.cff
```

### Data

The folder `data` contains the data used in this project:
* `structured_data` contains the structured data in CSV, JSON and RDF formats, representing various entities such as companies, individuals, and administrative entities.
* `scanned_images` contains the scanned images of the original book pages in JPEG format with 400 dpi.
* `ocr_output` contains the raw text output from the Optical Character Recognition (OCR) process, saved in plain text files.
* `models` contain the OCR-models

**Data availability statement:** Data used in this project are freely available under the CC BY license.

### Docs

The folder `docs` contains a documentation for this project including
* talks
   * **Extracting research data from historical documents with eScriptorium and Python** by Jan Kamlah, Thomas Schmidt and Renat Shigapov at [NFDI Focused Tutorial on Capturing, Enriching, Disseminating Research Data Objects](https://www.berd-nfdi.de/focused-tutorial-on-capturing-enriching-disseminating-research-data-objects). The presentations in English and German are available at [https://doi.org/10.5281/zenodo.7373134](https://doi.org/10.5281/zenodo.7373134).
   * Kamlah, Jan, & Shigapov, Renat. (2023, May 5). **The German Production Pipeline: Mannheim - OCR & Knowledge Graphs.** Zenodo. https://doi.org/10.5281/zenodo.7900133
* `sparql_examples` contains SPARQL query examples for the MBI-KG

### Code

The folder `code` contains codes used in this project:
* book2entities.py

**Code availability statement:** Codes used in this project are openly available under MIT license.

## How to contribute

Thank you for your interest in contributing to MBI knowledge graph. All contributions are welcome.

To get started, please follow these steps:

1. Fork the repository or clone it to your local machine.
2. Create a new branch for your changes.
3. Make your changes and commit them with clear commit messages.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

More info in [CONTRIBUTING.md](https://github.com/UB-Mannheim/MBI-KG/blob/main/CONTRIBUTING.md).

## License

This work is licensed under the MIT license (code) and Creative Commons Attribution 4.0 International license (for everything else). You are free to share and adapt the material for any purpose, even commercially, as long as you provide attribution (see CITATION.cff).