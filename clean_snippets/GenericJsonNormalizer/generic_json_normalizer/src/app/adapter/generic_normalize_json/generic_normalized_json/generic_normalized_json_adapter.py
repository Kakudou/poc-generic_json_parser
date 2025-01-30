""" This module use the usecase GenericNormalizedJson"""
from typing\
    import Dict

from generic_json_normalizer.src\
    import STORAGE_ENGINE

from generic_json_normalizer.src.utils.container\
    import Container
from generic_json_normalizer.src.generic_json_normalizer.usecase.\
    generic_normalize_json.generic_normalized_json.generic_normalized_json_inputport_builder\
    import GenericNormalizedJsonInputPortBuilder


class GenericNormalizedJsonAdapter:
    """This class gonna take the input, sanitize and give it to the usecase.

    Functions:
    ----------
    execute: staticmethod
        will consume the usecase GenericNormalizedJson.

    """

    @staticmethod
    def execute(inputs: Dict, storage_engine=STORAGE_ENGINE):
        """This function will convert inputs into GenericNormalizedJsonInputPort
        with the use of GenericNormalizedJsonInputPortBuilder.
        Then this contract will be gave to GenericNormalizedJson usecase.
        In return we should obtain the contract GenericNormalizedJsonOutputPort

        Parameters:
        -----------
        inputs: Dict
            a Dict containing the inputs:
            mapping_description: str
                The mapping description we want to apply to the data json.
            input_json: str
                The json data we want to normalize.

        Returns:
        --------
        GenericNormalizedJson_oc
            the output contract of the usecase GenericNormalizedJson

        """

        sanitize_mapping_description = inputs["mapping_description"]
        sanitize_input_json = inputs["input_json"]

        generic_normalized_json_icb = GenericNormalizedJsonInputPortBuilder()
        generic_normalized_json_ic = generic_normalized_json_icb\
            .create()\
            .with_mapping_description(sanitize_mapping_description)\
            .with_input_json(sanitize_input_json)\
            .build()

        generic_normalized_json_oc = Container\
            .get_usecase_repo("GenericNormalizedJson", storage_engine)\
            .execute(generic_normalized_json_ic)

        return generic_normalized_json_oc
