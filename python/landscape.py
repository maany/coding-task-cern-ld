import logging

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

    def load(self, input):
        entities = input.split("\n\n")
        for entity in entities:
            entity_info = entity.split("\n")
            entity_type = entity_info[0]
            if entity_type not in Landscape.registered_entity_schemas.keys():
                logger.warning(f"No registered schema found for {entity_type}. Skipping!")
                continue

            logger.debug(f"Found schema for {entity_type}: {Landscape.registered_entity_schemas[entity_type]}")


