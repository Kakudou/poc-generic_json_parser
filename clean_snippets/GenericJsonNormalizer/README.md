# GenericJsonNormalizer

---------------------------------------------------

<center><a href="https://gitmoji.carloscuesta.me">
  <img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square" alt="Gitmoji">
</a></center>

---------------------------------------------------

## TL;DR

[[_TOC_]]

# Generic JSON Parser

## Overview

This project provides a CLI tool and a library for parsing, normalizing, and transforming JSON data into a structured format based on user-defined mapping rules. The transformation process is guided by JSONPath expressions (via `jq`-like syntax), making it easy to extract, map, and restructure JSON input into any desired format.

## Features

- **CLI Tool & Library**: Use it as a standalone command-line tool or integrate it into your Python project.
- **Flexible Mapping Rules**: Define transformation rules using JSONPath expressions.
- **Input Normalization**: Ensure consistency by converting raw JSON into a structured format.
- **Customizable Output**: Adapt the parser for different use cases by modifying the mapping rules.
- **Lightweight & Extensible**: No heavy dependencies, easy to extend for additional functionality.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Kakudou/poc-generic_json_parser.git
cd generic_json_parser/clean_snippets/GenericJsonNormalizer
python -m venv .venv --prompt=GenericJsonNormalizer
pip install .
```

## Usage

### As a CLI Tool

```bash
GenericJsonNormalizer --json input.json --mapping rules.json  [--output output.json]
```

- `input.json`: The JSON file to be parsed.
- `rules.json`: The mapping file describing how fields should be transformed.
- `output.json`: The output file to write the transformed JSON data (optional).
    If not provided, the output will be printed to the console with indent=2.

### As a Library

```python
from generic_json_normalizer.src.app.adapter.generic_normalize_json.generic_normalized_json.generic_normalized_json_adapter import GenericNormalizedJsonAdapter


inputs = {
    "mapping_description": mapping_description_as_str,
    "input_json": input_json_as_str,
}

contract = GenericNormalizedJsonAdapter.execute(inputs)

if contract.error:
    logging.error(f"An error occurred: {contract.error}")
    return 1

print(json_dumps(ast_literal_eval(contract.generic_normalized_json), indent=2))

```

## Mapping Rules Format

The mapping rules file (`rules.json`) defines how JSON fields should be extracted and mapped. Example:

```json
{
    "jq_root": ".[] | (.new[]?, .updated[]?) |",
   "vulnerability": {
         "name": ".cveId",
         "external_references": {
             "source_name": (".cveId", lambda x: "url"),
             "url": ".cveOrgLink"
         }
   }
}
```

This would transform:

```json
[
  {
    "fetchTime": "2025-01-29T10:36:35.834Z",
    "numberOfChanges": 1,
    "new": [
      {
        "cveId": "CVE-2025-0762",
        "cveOrgLink": "https://www.cve.org/CVERecord?id=CVE-2025-0762",
        "githubLink": "https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2025/0xxx/CVE-2025-0762.json",
        "dateUpdated": "2025-01-29T10:33:45.673Z"
      }
    ],
    "updated": [],
    "error": []
  },
  {...}
]
```

into:

```json
[
  {
    "vulnerability": {
      "name": "CVE-2025-0762",
      "external_references": {
        "source_name": "url",
        "url": "https://www.cve.org/CVERecord?id=CVE-2025-0762"
      }
    }
  },
  {...}
]
```

## Contributions

Contributions are welcome! Feel free to submit pull requests or open issues.

## License

This project is licensed under the MIT License.


