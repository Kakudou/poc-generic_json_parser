""""This module define the output contract to create a GenericNormalizedJson"""
from dataclasses\
    import dataclass


@dataclass
class GenericNormalizedJsonOutputPort:
    """This class defined the attributes the adapter will get

    Attributes:
    -----------
    error: str
        if an error happened during the usecase
    generic_normalized_json: str
        The normalized json data.

    """

    error: str = None
    generic_normalized_json: str = None
