""""This module define the input contract to create a GenericNormalizedJson"""
from dataclasses\
    import dataclass


@dataclass
class GenericNormalizedJsonInputPort:
    """"This class define the necessary attributes to create a GenericNormalizedJson

    Attributes:
    -----------
    mapping_description: str
        The mapping description we want to apply to the data json.
    input_json: str
        The json data we want to normalize.

    """

    mapping_description: str = None
    input_json: str = None
