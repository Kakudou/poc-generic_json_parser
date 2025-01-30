from sys import exit
from argparse import ArgumentParser
from json import dumps as json_dumps
from ast import literal_eval as ast_literal_eval

import logging

from generic_json_normalizer.src.app.adapter.generic_normalize_json.generic_normalized_json.generic_normalized_json_adapter import GenericNormalizedJsonAdapter

logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def generic_json_normalizer():
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--json", required=True, help="Path to input JSON file")
    argument_parser.add_argument("--mapping", required=True, help="Path to mapping description file")
    argument_parser.add_argument("--output", required=False, help="Path to output JSON file")

    parsed_arguments = argument_parser.parse_args()

    with open(parsed_arguments.json, "r") as json_file:
        input_json = json_file.read()
    with open(parsed_arguments.mapping, "r") as mapping_file:
        mapping_description = mapping_file.read()

    inputs = {
        "mapping_description": mapping_description,
        "input_json": input_json,
    }

    contract = GenericNormalizedJsonAdapter.execute(inputs)

    if contract.error:
        logging.error(f"An error occurred: {contract.error}")
        return 1

    if parsed_arguments.output:
        with open(parsed_arguments.output, "w") as output_file:
            output_file.write(json_dumps(ast_literal_eval(contract.generic_normalized_json), indent=2))
    else:
        print(json_dumps(ast_literal_eval(contract.generic_normalized_json), indent=2))


if __name__ == "__main__":
    try:
        exit(generic_json_normalizer())
    except Exception as e:
        logging.error(f"Exception occurred: {e}", exc_info=True)
        exit(1)
