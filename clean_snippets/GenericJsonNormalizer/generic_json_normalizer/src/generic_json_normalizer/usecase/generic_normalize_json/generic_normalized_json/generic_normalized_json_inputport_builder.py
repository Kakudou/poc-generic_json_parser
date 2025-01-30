"""This module is the builder that ensure the filling of the input contract"""
from dataclasses\
    import dataclass
from typing\
    import Any
from generic_json_normalizer.src.generic_json_normalizer.usecase.\
    generic_normalize_json.generic_normalized_json.generic_normalized_json_inputport\
    import GenericNormalizedJsonInputPort


@dataclass
class GenericNormalizedJsonInputPortBuilder:
    """This class defined the function to easily build the input contract

    Attributes:
    -----------
    __input: GenericNormalizedJsonInputPort
        the input contract

    Functions:
    ----------
    create:
        create the input contract
    with_mapping_description: str
        fill the mapping_description in the contract
    with_input_json: str
        fill the input_json in the contract
    build:
        build the final input contract

    """

    __input: Any = None

    def create(self):
        """ This function create the empty contract

        Returns:
        --------
        GenericNormalizedJsonInputPortBuilder
            this builder with the contract to fill

        """

        self.__input = GenericNormalizedJsonInputPort()
        return self

    def with_mapping_description(self, mapping_description: str):
        """ This function fill the mapping_description in the contract

        Parameters:
        -----------
        mapping_description: str
            the mapping_description of the GenericNormalizedJson

        Returns:
        --------
        GenericNormalizedJsonOutputPortBuilder
            this builder with the contract to fill

        """

        self._validate_mapping_description(mapping_description)
        self.__input.mapping_description = mapping_description
        return self

    def _validate_mapping_description(self, mapping_description: str):
        """ This function check the  validity of mapping_description in the contract

        Parameters:
        -----------
        mapping_description: str
            the mapping_description of the GenericNormalizedJson

        Returns:
        --------

        """
        if not mapping_description:
            raise ValueError("mapping_description is empty")

    def with_input_json(self, input_json: str):
        """ This function fill the input_json in the contract

        Parameters:
        -----------
        input_json: str
            the input_json of the GenericNormalizedJson

        Returns:
        --------
        GenericNormalizedJsonOutputPortBuilder
            this builder with the contract to fill

        """

        self._validate_input_json(input_json)
        self.__input.input_json = input_json
        return self

    def _validate_input_json(self, input_json: str):
        """ This function check the  validity of input_json in the contract

        Parameters:
        -----------
        input_json: str
            the input_json of the GenericNormalizedJson

        Returns:
        --------

        """
        if not input_json:
            raise ValueError("input_json is empty")

    def build(self) -> GenericNormalizedJsonInputPort:
        """ This function return the filled contract

        Returns:
        --------
        GenericNormalizedJsonInputPort
            the contract filled

        """

        self._validate_mapping_description(self.__input.mapping_description)
        self._validate_input_json(self.__input.input_json)

        return self.__input
