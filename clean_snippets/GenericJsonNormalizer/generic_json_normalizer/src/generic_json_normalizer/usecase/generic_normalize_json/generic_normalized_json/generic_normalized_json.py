"""This module is the core logic to create a Entity"""
from dataclasses\
    import dataclass
from typing\
    import Any

from json\
    import loads as json_loads
from jq\
    import compile as jq_compile

from generic_json_normalizer.src.generic_json_normalizer.usecase.\
    generic_normalize_json.generic_normalized_json.generic_normalized_json_inputport\
    import GenericNormalizedJsonInputPort
from generic_json_normalizer.src.generic_json_normalizer.usecase.\
    generic_normalize_json.generic_normalized_json.generic_normalized_json_outputport_builder\
    import GenericNormalizedJsonOutputPortBuilder
from generic_json_normalizer.src.generic_json_normalizer.usecase.\
    generic_normalize_json.generic_normalized_json.generic_normalized_json_outputport\
    import GenericNormalizedJsonOutputPort

from generic_json_normalizer.src.generic_json_normalizer.entity.generic_normalize_json.generic_normalized_json\
    import GenericNormalizedJson as GenericNormalizedJsonEntity


@dataclass
class GenericNormalizedJson:
    """This class is the usecase to create a Entity

    Attributes:
    -----------
    __output: GenericNormalizedJsonOutputPort
        is the outputport information who gonna travel to the adapter

    Functions:
    ----------
    __init__:
        classical constructor
    execute:
        execute the usecase logic

    """

    __output: Any = None

    def __init__(self, implemented_gateway):
        """This function is the constructor particularity:
        the container utils class give it the good implemented_gateway

        Parameters:
        -----------
        implemented_gateway:
            The implemented_gateway for the storage engine we want
        """

        self.gateway = implemented_gateway
        self.builder = GenericNormalizedJsonOutputPortBuilder()

    def execute(self, inputp: GenericNormalizedJsonInputPort) -> GenericNormalizedJsonOutputPort:
        """This function will from the inputport create a GenericNormalizedJson
        and save it if none with the same identifier is found.
        And then return the appropriate outputport.

        Parameters:
        -----------
        inputport: GenericNormalizedJsonInputPort
            the inputport who come from the adapter

        Returns:
        --------
        GenericNormalizedJsonOutputPort:
            The output contract

        """

        executed = False
        generic_normalized_json = None
        error = None

        mapping_description = inputp.mapping_description
        input_json = inputp.input_json

        identifier = (mapping_description, input_json)

        json = json_loads(input_json)
        mapping = eval(mapping_description)
        normalized_json_data = self.__normalize_json_data(json, mapping)

        generic_normalized_json = self.gateway.exist_by_identifier(identifier)

        if generic_normalized_json:
            error = "The KillChainPhase you want, already exist"
            self.__output = self.builder.create().with_error(error).build()
        else:
            generic_normalized_json = GenericNormalizedJsonEntity()
            generic_normalized_json.mapping_description = mapping_description
            generic_normalized_json.input_json = input_json
            generic_normalized_json.generic_normalized_json = normalized_json_data

            executed = self.gateway.save(generic_normalized_json)

        if executed:
            self.__output = self.builder.create()\
                                .with_generic_normalized_json(normalized_json_data)\
                                .build()

        elif not executed and generic_normalized_json is None:
            if error is None:
                error = "An error occured during persistence"
            self.__output = self.builder.create().with_error(error).build()

        return self.__output

    def __extract_lambda_functions_from_mapping(self, mapping_data):
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


    def __apply_lambda_functions_to_data(self, json_data, mapping):
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


        for composite_key, transformation_function in self.__extract_lambda_functions_from_mapping(mapping):
            target_object_key, target_field_key = composite_key.split("§")  # Extract object and field names
            for json_entry in json_data:
                recursive_application(json_entry, target_object_key, target_field_key, transformation_function)

        return json_data

    def __build_jq_output_template(self, mapping_template, jq_root_path=""):
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
                sub_output, jq_root_path = self.__build_jq_output_template(sub_template, jq_root_path)
                jq_output_parts.append(f'"{parent_key}": {{ {sub_output} }}')
            elif isinstance(sub_template, tuple):
                jq_output_parts.append(f'"{parent_key}": {sub_template[0]}')

        return ", ".join(jq_output_parts), jq_root_path

    def __contains_null_values(self, json_object):
        """
        Check if the given JSON object contains null values.
        """
        if isinstance(json_object, dict):
            return any(self.__contains_null_values(value) for value in json_object.values())
        elif isinstance(json_object, list):
            return any(self.__contains_null_values(item) for item in json_object)
        return json_object is None

    def __normalize_json_data(self, json_data, mapping_data):
        """
        Normalize JSON data based on mapping configuration using JQ processing.
        """
        jq_output_template, jq_root_path = self.__build_jq_output_template(mapping_data)
        jq_query_string = f"""
        [ {jq_root_path} {{ {jq_output_template} }} ]
        """
        jq_transformed_data = jq_compile(jq_query_string).input(json_data).all()

        # Remove empty and null values from processed data
        filtered_json_data = jq_compile(
            '.[][] | walk(select(. != {} and . != null and . != "null"))'
        ).input(jq_transformed_data).all()

        final_transformed_data = self.__apply_lambda_functions_to_data(filtered_json_data, mapping_data)

        return str([entry for entry in final_transformed_data if not self.__contains_null_values(entry)])
