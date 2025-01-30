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
    Extract transformation functions (lambdas) from the mapping data using a generator.
    """
    def recursive_extraction(mapping_dictionary, parent_key=""):
        for key, value in mapping_dictionary.items():
            if isinstance(value, tuple):
                composite_key = f"{parent_key}§{key}"
                yield (composite_key, value[1])  # Yield transformation function
            elif isinstance(value, dict):
                yield from recursive_extraction(value, key)

    return recursive_extraction(mapping_data)


def apply_lambda_functions_to_data(json_data, mapping):
    """
    Apply extracted lambda functions to the corresponding JSON fields using a generator for recursive application.
    """
    def recursive_application(json_entry, target_object_key, target_field_key, transformation_function):
        if isinstance(json_entry, dict):
            if target_object_key in json_entry:
                target_object = json_entry[target_object_key]
                if isinstance(target_object, dict):
                    # Apply transformation to the target field directly
                    target_object[target_field_key] = transformation_function(
                        target_object.get(target_field_key, None)
                    )
            # Avoid unnecessary nested checks by directly traversing sub-entries if needed
            else:
                for sub_entry in json_entry.values():
                    if isinstance(sub_entry, dict):
                        recursive_application(sub_entry, target_object_key, target_field_key, transformation_function)


    for composite_key, transformation_function in extract_lambda_functions_from_mapping(mapping):
        target_object_key, target_field_key = composite_key.split("§")  # Extract object and field names
        for json_entry in json_data:
            recursive_application(json_entry, target_object_key, target_field_key, transformation_function)

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

    final_transformed_data = apply_lambda_functions_to_data(filtered_json_data, mapping_data)

    return [entry for entry in final_transformed_data if not contains_null_values(entry)]

def main_routine(json_file_path, mapping_file_path):
    json_data, mapping_data = load_json_and_mapping(json_file_path, mapping_file_path)
    normalized_json_data = normalize_json_data(json_data, mapping_data)
    return normalized_json_data

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--json", required=True, help="Path to JSON file")
    argument_parser.add_argument("--mapping", required=True, help="Path to mapping file")

    parsed_arguments = argument_parser.parse_args()


    result = main_routine(parsed_arguments.json, parsed_arguments.mapping)
    print(json.dumps(result, indent=2))


