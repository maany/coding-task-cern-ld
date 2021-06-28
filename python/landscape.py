import logging

from python.landscape_model_framework.exceptions import SchemaNotRegisteredException, InvalidSyntax

logger = logging.getLogger(__name__)


class Landscape:
    """
    Class providing functionality to parse input data into a data entities
    and functionality to access and print those entities
    """
    registered_loaders = {}
    registered_entity_schemas = {}

    def __init__(self):
        self.elements = []
        self.entities_with_id = {}
        self.entities_sans_id = []

    @staticmethod
    def __parse_entity_attributes(dummy_entity, attribute_list):
        expression_attrs = {}
        regular_attrs = {}
        invalid_attrs = []
        for attribute in attribute_list:
            if ':=' in attribute:
                attr_and_val = attribute.split(':=')
                expression_attrs[attr_and_val[0]] = attr_and_val[1]

            elif '=' in attribute:
                attr_and_val = attribute.split('=')
                regular_attrs[attr_and_val[0]] = attr_and_val[1]
            else:
                invalid_attrs.append(attribute)

        dummy_entity['regular_attrs'] = regular_attrs
        dummy_entity['expression_attrs'] = expression_attrs

        if len(invalid_attrs) > 0:
            raise InvalidSyntax(f'Could not parse the following attributes: {invalid_attrs}')
        return expression_attrs, regular_attrs

    def __parse_entity(self, entity):
        entity_info = entity.split("\n")
        entity_type = entity_info[0]
        if entity_type not in Landscape.registered_entity_schemas.keys():
            raise SchemaNotRegisteredException(entity_type=entity_type)

        if entity_info[1].startswith('#'):
            entity_id = entity_info[1][1:]
            entity_attributes = entity_info[2:]
        else:
            entity_id = None
            entity_attributes = entity_info[1:]

        dummy_entity = {
            "id": entity_id,
            "type": entity_type
        }

        try:
            self.__parse_entity_attributes(dummy_entity, entity_attributes)
        except InvalidSyntax as ex:
            logger.error(f"Could not correctly parse attributes of {dummy_entity}")
        finally:
            return entity_id, dummy_entity

    def load(self, input):
        entities = input.split("\n\n")
        for entity in entities:
            try:
                dummy_entity_id, dummy_entity = self.__parse_entity(entity)
                if dummy_entity_id is not None:
                    self.entities_with_id[dummy_entity_id] = dummy_entity
                else:
                    self.entities_sans_id.append(dummy_entity)
            except SchemaNotRegisteredException as ex:
                logger.warning(f"No registered schema found for {entity}. Skipping!")
                continue
            except Exception as ex:
                logger.warning(f"Unexpected error while parsing {entity}. Skipping!")
        pass