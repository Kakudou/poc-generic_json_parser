"""This module handle the data access in memory"""
from hashlib\
    import sha256
from typing\
    import List

from generic_json_normalizer.src.utils.\
    singleton\
    import Singleton
from generic_json_normalizer.src.app.\
    dto.generic_normalize_json.generic_normalized_json_dto\
    import GenericNormalizedJsonDTO
from generic_json_normalizer.src.generic_json_normalizer.gateway.\
    generic_normalize_json.generic_normalized_json_gateway\
    import GenericNormalizedJsonGateway
from generic_json_normalizer.src.generic_json_normalizer.entity.\
    generic_normalize_json.generic_normalized_json\
    import GenericNormalizedJson
from generic_json_normalizer.src.app.\
    repository.inmemory.inmemory_persist\
    import InMemoryPersist


@Singleton
class GenericNormalizedJsonINMEMORYRepository(GenericNormalizedJsonGateway):
    """"This class implement the GenericNormalizedJsonGateway

    Functions:
    ----------
    __init__:
        will get the dict from InMemoryPersist
    _generate_id:
        will generate an hash from identifier for storage
    save:
        will 'save' the GenericNormalizedJson inmemory dict
    exist_by_identifier:
        will check if an GenericNormalizedJson with this identifier exist
    update_by_identifier:
        will 'update' the GenericNormalizedJson inmemory dict
    find_all:
        will search all GenericNormalizedJson
    find_by_identifier:
        will search an GenericNormalizedJson by his identifier
    destroy_by_identifier:
        will delete an GenericNormalizedJson by his identifier
    _convert_to_dto:
        convert core GenericNormalizedJson to GenericNormalizedJsonDTO
    _convert_to_entity:
        convert GenericNormalizedJsonDTO to core GenericNormalizedJson
    """

    def __init__(self):
        """Init InMemoryPersist who will be used for inmemory storage"""

        self.__persists = InMemoryPersist()
        self.__persists.generic_normalized_jsons = {}

    def _generate_id(self, identifier) -> str:
        """This function will generate an ID for the entity
        base on his identifier

        Returns:
        --------
        str
            the identifier hash

        """

        id = sha256(str(identifier).encode()).hexdigest()

        return id

    def save(self, generic_normalized_json: GenericNormalizedJson) -> bool:
        """This function will save GenericNormalizedJson as GenericNormalizedJsonDTO

        Parameters:
        -----------
        generic_normalized_json: GenericNormalizedJson
            The GenericNormalizedJson that we will be saved and convert as GenericNormalizedJsonDTO

        Returns:
        --------
        bool
            True if saved

        """

        saved = False

        generic_normalized_json_dto = self._convert_to_dto(generic_normalized_json)
        self.__persists.generic_normalized_jsons[generic_normalized_json_dto.id] = generic_normalized_json_dto

        saved = True

        return saved

    def exist_by_identifier(self, identifier) -> bool:
        """This function will check GenericNormalizedJson existence by is identifier

        Parameters:
        -----------
        identifier: str
            The identifier for the GenericNormalizedJson to check

        Returns:
        --------
        bool
            True if exist

        """

        exist = False

        hash_id = sha256(str(identifier).encode()).hexdigest()

        try:
            found = self.__persists.generic_normalized_jsons[hash_id]
        except KeyError:
            found = None

        if found is not None:
            exist = True

        return exist

    def update_by_identifier(self, identifier: str, generic_normalized_json: GenericNormalizedJson) -> bool:
        """This function will update GenericNormalizedJson

        Parameters:
        -----------
        identifier: str
            the identifier for the GenericNormalizedJson to update
        generic_normalized_json: GenericNormalizedJson
            The GenericNormalizedJson that we will be updated

        Returns:
        --------
        bool
            True if updated

        """

        updated = False

        generic_normalized_json_dto = self._convert_to_dto(generic_normalized_json)
        self.__persists.generic_normalized_jsons[generic_normalized_json_dto.id] = generic_normalized_json_dto

        updated = True

        return updated

    def find_all(self) -> List[GenericNormalizedJson]:
        """This function will find all GenericNormalizedJson

        Parameters:
        -----------

        Returns:
        --------
        List[GenericNormalizedJson]:
            all GenericNormalizedJson

        """

        generic_normalized_jsons = []
        for generic_normalized_json_id in self.__persists.generic_normalized_jsons:
            generic_normalized_json_dto = self.__persists.generic_normalized_jsons[generic_normalized_json_id]
            generic_normalized_json = self._convert_to_entity(generic_normalized_json_dto)
            generic_normalized_jsons.append(generic_normalized_json)

        return generic_normalized_jsons

    def find_by_identifier(self, identifier: str) -> GenericNormalizedJson:
        """This function will find GenericNormalizedJson by is identifier

        Parameters:
        -----------
        identifier: str
            The identifier for GenericNormalizedJson to find

        Returns:
        --------
        GenericNormalizedJson:
            The GenericNormalizedJson

        """

        generic_normalized_json = None

        hash_id = sha256(str(identifier).encode()).hexdigest()

        try:
            generic_normalized_json_dto = self.__persists.generic_normalized_jsons[hash_id]
        except KeyError:
            generic_normalized_json_dto = None

        if generic_normalized_json_dto is not None:
            generic_normalized_json = self._convert_to_entity(generic_normalized_json_dto)

        return generic_normalized_json

    def destroy_by_identifier(self, identifier: str) -> bool:
        """This function will delete GenericNormalizedJson

        Parameters:
        -----------
        identifier: str
            The identifier for the GenericNormalizedJson to delete

        Returns:
        --------
        bool
            True if deleted

        """

        deleted = False

        generic_normalized_json_id = self._generate_id(identifier)
        del self.__persists.generic_normalized_jsons[generic_normalized_json_id]

        deleted = True

        return deleted

    def _convert_to_dto(self, generic_normalized_json: GenericNormalizedJson) -> GenericNormalizedJsonDTO:
        """This function will convert GenericNormalizedJson to a GenericNormalizedJsonDTO

        Parameters:
        -----------
        generic_normalized_json: GenericNormalizedJson
            Entity GenericNormalizedJson as seen by the core

        Returns:
        --------
        GenericNormalizedJsonDTO
            the GenericNormalizedJsonDTO ready to be persist

        """

        identifier = (generic_normalized_json.mapping_description, generic_normalized_json.input_json)

        generic_normalized_json_dto = GenericNormalizedJsonDTO()
        generic_normalized_json_dto.id = self._generate_id(identifier)
        generic_normalized_json_dto.mapping_description = generic_normalized_json.mapping_description
        generic_normalized_json_dto.input_json = generic_normalized_json.input_json
        generic_normalized_json_dto.generic_normalized_json = generic_normalized_json.generic_normalized_json

        return generic_normalized_json_dto

    def _convert_to_entity(self, generic_normalized_json_dto: GenericNormalizedJsonDTO) -> GenericNormalizedJson:
        """This function will convert a GenericNormalizedJsonDTO to GenericNormalizedJson

        Parameters:
        -----------
        GenericNormalizedJsonDTO
            the GenericNormalizedJsonDTO ready to be persist

        Returns:
        --------
        generic_normalized_json: GenericNormalizedJson
            Entity GenericNormalizedJson as seen by the core

        """

        generic_normalized_json = GenericNormalizedJson()
        generic_normalized_json.mapping_description = generic_normalized_json_dto.mapping_description
        generic_normalized_json.input_json = generic_normalized_json_dto.input_json
        generic_normalized_json.generic_normalized_json = generic_normalized_json_dto.generic_normalized_json

        return generic_normalized_json
