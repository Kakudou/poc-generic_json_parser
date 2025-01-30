"""This module is the builder that ensure the filling of the output contract"""
from dataclasses\
    import dataclass
from typing\
    import Any
from generic_json_normalizer.src.generic_json_normalizer.usecase.\
    generic_normalize_json.generic_normalized_json.generic_normalized_json_outputport\
    import GenericNormalizedJsonOutputPort


@dataclass
class GenericNormalizedJsonOutputPortBuilder:
    """This class defined the function to easily build the output contract

    Attributes:
    -----------
    __output: GenericNormalizedJsonOutputPort
        the output contract

    Functions:
    ----------
    create:
        create the output contract
    with_generic_normalized_json: str
        fill the generic_normalized_json in the contract
    with_error:
        fill the possible usecase error
    build:
        build the final output contract

    """

    __output: Any = None

    def create(self):
        """ This function create the empty contract

        Returns:
        --------
        GenericNormalizedJsonOutputPortBuilder
            this builder with the contract to fill

        """

        self.__output = GenericNormalizedJsonOutputPort()
        return self

    def with_generic_normalized_json(self, generic_normalized_json: str):
        """ This function fill the generic_normalized_json in the contract

        Parameters:
        -----------
        generic_normalized_json: str
            the generic_normalized_json of the GenericNormalizedJson

        Returns:
        --------
        GenericNormalizedJsonOutputPortBuilder
            this builder with the contract to fill

        """

        self.__output.generic_normalized_json = generic_normalized_json
        return self

    def with_error(self, error: str):
        """ This function fill the error in the contract

        Parameters:
        -----------
        error: str
            the error of the usecase

        Returns:
        --------
        GenericNormalizedJsonOutputPortBuilder
            this builder with the contract to fill

        """

        self.__output.error = error
        return self

    def build(self) -> GenericNormalizedJsonOutputPort:
        """ This function return the filled contract

        Returns:
        --------
        GenericNormalizedJsonOutputPort
            the contract filled

        """

        return self.__output
