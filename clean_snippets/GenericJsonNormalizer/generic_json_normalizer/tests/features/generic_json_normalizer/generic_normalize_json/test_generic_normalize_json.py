import os

from pytest import mark
from pytest_bdd\
    import scenario, given, when, then, parsers


from generic_json_normalizer.src.utils.container\
    import Container

from generic_json_normalizer.src.generic_json_normalizer.usecase.\
    generic_normalize_json.generic_normalized_json.generic_normalized_json_inputport_builder\
    import GenericNormalizedJsonInputPortBuilder as InputPortBuilder


STORAGE_ENGINE = "INMEMORY"
__fullpath = os.path.dirname(os.path.abspath(__file__))


@mark.order(1)
@scenario(f"{__fullpath.split('/GenericJsonNormalizer/')[0]}"
          "/GenericJsonNormalizer/generic_json_normalizer"
          "/features/generic_json_normalizer/generic_normalize_json/generic_normalize_json.feature",
          "We have an input json, and we wrote a mapping file describing the output we want, then we should obtain the output json filled with the good data.")
def test_generic_normalize_json():
    pass


@given(parsers.parse("I have an {input_json} as a str, and an {mapping_description} as a str."), target_fixture="context")
def given_generic_normalize_json(input_json, mapping_description):
    input_contract = InputPortBuilder()\
        .create()\
        .with_input_json(input_json)\
        .with_mapping_description(mapping_description)\
        .build()

    return {
        "input_json": input_json,
        "mapping_description": mapping_description,
        "input_contract": input_contract
    }


@when(parsers.parse("I apply the mapping description over the json data."))
def when_generic_normalize_json(context, ):
    usecase = Container.get_usecase_repo("GenericNormalizedJson", STORAGE_ENGINE)
    output_contract = usecase.execute(context["input_contract"])
    context["output_contract"] = output_contract


@then(parsers.parse("I obtain the desire {normalized_json}"))
def then_generic_normalize_json(context, normalized_json):
    import json
    print(json.dumps(context["output_contract"].generic_normalized_json))
    print(json.dumps(normalized_json))

#?     print(context["output_contract"].generic_normalized_json)

    assert context["output_contract"]\
        .generic_normalized_json == normalized_json
