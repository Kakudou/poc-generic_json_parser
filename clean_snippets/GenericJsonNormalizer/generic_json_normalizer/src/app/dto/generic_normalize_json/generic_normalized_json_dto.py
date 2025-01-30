"""This module is the GenericNormalizedJsonDTO that will be persist"""
from dataclasses\
    import dataclass


@dataclass
class GenericNormalizedJsonDTO:
    """This class defined the attributes that we want to be persist

    Attributes:
    -----------
    __id: str
        The hash of the identifier of GenericNormalizedJson: (mapping_description, input_json)
    __mapping_description: str
        The string representation of the normalized json data we want to generate.
    __input_json: str
        The string representation of the data json we want to normalize.
    __generic_normalized_json: str
        The string representation of the normalized json data we generated.

    Functions:
    ----------
    Getter and Setter for above attributes
    """

    __id: str = None
    __mapping_description: str = None
    __input_json: str = None
    __generic_normalized_json: str = None

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id: str):
        self.__id = id

    @property
    def mapping_description(self) -> str:
        return self.__mapping_description

    @mapping_description.setter
    def mapping_description(self, mapping_description: str):
        self.__mapping_description = mapping_description

    @property
    def input_json(self) -> str:
        return self.__input_json

    @input_json.setter
    def input_json(self, input_json: str):
        self.__input_json = input_json

    @property
    def generic_normalized_json(self) -> str:
        return self.__generic_normalized_json

    @generic_normalized_json.setter
    def generic_normalized_json(self, generic_normalized_json: str):
        self.__generic_normalized_json = generic_normalized_json
