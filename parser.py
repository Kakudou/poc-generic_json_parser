import json
import jq
import argparse


def load_json_and_mapping(json_file_path, mapping_file_path):
    """
    Load JSON data and mapping file from the given file paths.
    """
    json_data = None
    mapping_data = None
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
    with open(mapping_file_path, 'r') as file:
        mapping_data = file.read()
    return json_data, eval(mapping_data)


def extract_lambda_functions_from_mapping(mapping_data):
    """
    Extract transformation functions (lambdas) from the mapping data.
    """
    lambda_functions = set()

    def recursive_extraction(mapping_dictionary, parent_key=""):
        for key, value in mapping_dictionary.items():
            if isinstance(value, tuple):
                composite_key = f"{parent_key}§{key}"
                lambda_functions.add((composite_key, value[1]))  # Store transformation function
            elif isinstance(value, dict):
                recursive_extraction(value, key)

    recursive_extraction(mapping_data)
    return lambda_functions


def apply_lambda_functions_to_data(json_data, lambda_functions):
    """
    Apply extracted lambda functions to the corresponding JSON fields.
    """
    def recursive_application(json_data, target_object_key, target_field_key, transformation_function):
        for json_entry in json_data:
            if isinstance(json_entry, dict):
                if target_object_key in json_entry:
                    json_entry[target_object_key][target_field_key] = transformation_function(
                        json_entry[target_object_key].get(target_field_key, None)
                    )
                else:
                    for sub_entry in json_entry.values():
                        if isinstance(sub_entry, dict) and target_object_key in sub_entry:
                            sub_entry[target_object_key][target_field_key] = transformation_function(
                                sub_entry[target_object_key].get(target_field_key, None)
                            )

    for composite_key, transformation_function in lambda_functions:
        target_object_key, target_field_key = composite_key.split("§")  # Extract object and field names
        recursive_application(json_data, target_object_key, target_field_key, transformation_function)

    return json_data


def build_jq_output_template(mapping_template, jq_root_path=""):
    """
    Construct the JQ output template from the mapping configuration.
    """
    jq_output_parts = []

    for parent_key, sub_template in mapping_template.items():
        if parent_key == "jq_root":
            jq_root_path = sub_template  # Define the root of the JQ query
        elif isinstance(sub_template, str):
            jq_output_parts.append(f'"{parent_key}": {sub_template}')
        elif isinstance(sub_template, dict):
            sub_output, jq_root_path = build_jq_output_template(sub_template, jq_root_path)
            jq_output_parts.append(f'"{parent_key}": {{ {sub_output} }}')
        elif isinstance(sub_template, tuple):
            jq_output_parts.append(f'"{parent_key}": {sub_template[0]}')

    return ", ".join(jq_output_parts), jq_root_path


def contains_null_values(json_object):
    """
    Check if the given JSON object contains null values.
    """
    if isinstance(json_object, dict):
        return any(contains_null_values(value) for value in json_object.values())
    elif isinstance(json_object, list):
        return any(contains_null_values(item) for item in json_object)
    return json_object is None


def normalize_json_data(json_data, mapping_data):
    """
    Normalize JSON data based on mapping configuration using JQ processing.
    """
    jq_output_template, jq_root_path = build_jq_output_template(mapping_data)
    jq_query_string = f"""
    [ {jq_root_path} {{ {jq_output_template} }} ]
    """
    jq_transformed_data = jq.compile(jq_query_string).input(json_data).all()

    # Remove empty and null values from processed data
    filtered_json_data = jq.compile(
        '.[][] | walk(select(. != {} and . != null and . != "null"))'
    ).input(jq_transformed_data).all()

    lambda_functions = extract_lambda_functions_from_mapping(mapping_data)
    final_transformed_data = apply_lambda_functions_to_data(filtered_json_data, lambda_functions)

    return [entry for entry in final_transformed_data if not contains_null_values(entry)]


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--json", required=True, help="Path to JSON file")
    argument_parser.add_argument("--mapping", required=True, help="Path to mapping file")
    parsed_arguments = argument_parser.parse_args()

    json_data, mapping_data = load_json_and_mapping(parsed_arguments.json, parsed_arguments.mapping)
    normalized_json_data = normalize_json_data(json_data, mapping_data)
    print(json.dumps(normalized_json_data, indent=2))

