import logging
import re

from python.landscape_model_framework.exceptions import (
    SchemaNotRegisteredException,
    InvalidSyntax,
)

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
    def __check_attribute_type(attributes, entity):
        additional_attributes = []
        invalid_type_attributes = []
        entity_type = entity["type"]
        if entity_type not in Landscape.registered_entity_schemas.keys():
            raise SchemaNotRegisteredException(entity_type=entity_type)
        schema = Landscape.registered_entity_schemas[entity_type]
        for attribute, val in attributes.items():
            try:
                schema[attribute](val)
            except (TypeError, ValueError) as e:
                logger.warning(
                    f"Value supplied for attribute {attribute} of {entity_type} is incompatible "
                    f"with {schema[attribute]}"
                )
                invalid_type_attributes.append(attribute)
            except KeyError as e:
                logger.warning(
                    f"Addition attribute {attribute} of entity {entity_type} will be ignored"
                )
                additional_attributes.append(attribute)
        return additional_attributes, invalid_type_attributes

    @staticmethod
    def __parse_entity_attributes(dummy_entity, attribute_list):
        expression_attrs = {}
        regular_attrs = {}
        all_attrs = {}
        invalid_attrs = []
        for attribute in attribute_list:
            if ":=" in attribute:
                attr_and_val = attribute.split(":=")
                expression_attrs[attr_and_val[0]] = attr_and_val[1]
                all_attrs[attr_and_val[0]] = attr_and_val[1]
            elif "=" in attribute:
                attr_and_val = attribute.split("=")
                regular_attrs[attr_and_val[0]] = int(attr_and_val[1])
                all_attrs[attr_and_val[0]] = int(attr_and_val[1])
            else:
                logger.warning(
                    f"Syntax error in line representing attribute {attribute} of {dummy_entity}."
                )
                invalid_attrs.append(attribute)

        dummy_entity["regular_attrs"] = regular_attrs
        dummy_entity["expression_attrs"] = expression_attrs
        dummy_entity["all_attrs"] = all_attrs

        if len(invalid_attrs) > 0:
            raise InvalidSyntax(
                f"Could not parse the following attributes: {invalid_attrs}"
            )

    def __parse_entity(self, entity):
        entity_info = entity.split("\n")
        entity_type = entity_info[0]

        if entity_info[1].startswith("#"):
            entity_id = int(entity_info[1][1:])
            entity_attributes = entity_info[2:]
        else:
            entity_id = None
            entity_attributes = entity_info[1:]

        dummy_entity = {"id": entity_id, "type": entity_type}

        try:
            self.__parse_entity_attributes(dummy_entity, entity_attributes)
            additional_parameters, invalid_parameters = self.__check_attribute_type(
                attributes=dummy_entity["regular_attrs"], entity=dummy_entity
            )
            final_regular_attrs = [
                attr
                for attr in dummy_entity["regular_attrs"]
                if attr not in additional_parameters or attr not in invalid_parameters
            ]
            dummy_entity["final_regular_attrs"] = final_regular_attrs
        except SchemaNotRegisteredException as ex:
            logger.error(
                f"Could not correctly parse attributes of {dummy_entity['type']} due to missing schema"
            )
        except InvalidSyntax:
            logger.error(f"syntax errors detected in {entity}")
        finally:
            return entity_id, dummy_entity

        for entity_id, expression_attr in all_expression_attrs.items():
            for dependent_attribute, expression in expression_attr.items():
                result = self.__evaluate_expression(
                    entity_id,
                    dependent_attribute,
                    expression,
                    all_entity_ids,
                    all_expression_attrs,
                    all_regular_attrs,
                )

            # except Exception:
            #     logger.error("Exception")
            # else:
            #     pass

    def load(self, input):
        dummy_entities_with_id = {}
        dummy_entities_without_id = []
        entities = input.strip().split("\n\n")

        # parse entities
        for entity in entities:
            dummy_entity_id, dummy_entity = self.__parse_entity(entity)
            if dummy_entity_id is not None:
                dummy_entities_with_id[dummy_entity_id] = dummy_entity
            else:
                dummy_entities_without_id.append(dummy_entity)

        # evaluate attributes for entities with an id
        dummy_entity_attributes_map = {
            entity_id: entity["all_attrs"]
            for entity_id, entity in dummy_entities_with_id.items()
        }
        max_passes = Landscape.num_attributes(dummy_entity_attributes_map)
        for entity_id, attributes in dummy_entity_attributes_map.items():
            for attr_name, attr_val in attributes.items():
                evaluated_val = Landscape.evaluate_attribute(
                    entity_id,
                    attr_name,
                    attr_val,
                    dummy_entity_attributes_map,
                    max_passes,
                )
                dummy_entity_attributes_map[entity_id][attr_name] = evaluated_val

        # evaluate attributes for entities without ids
        for entity in dummy_entities_without_id:
            all_attrs = entity["all_attrs"]
            for attr_name, attr_val in all_attrs.items():
                evaluated_val = Landscape.evaluate_attribute(
                    "no_id_temp", attr_name, attr_val, dummy_entity_attributes_map, 1
                )
                all_attrs[attr_name] = evaluated_val

        # generate landscape elements
        all_dummy_entities = [
            entity for entity_id, entity in dummy_entities_with_id.items()
        ]
        all_dummy_entities.extend(dummy_entities_without_id)

        for dummy_entity in all_dummy_entities:
            loader = None
            if dummy_entity["type"] in Landscape.registered_loaders:
                loader = Landscape.registered_loaders[dummy_entity["type"]]
            else:
                logger.warning(
                    f"No loader found for entity type {dummy_entity['type']}"
                )
                continue
            entity = loader(dummy_entity)
            self.elements.append(entity)

    @staticmethod
    def num_attributes(dummy_entity_attributes_map):
        sum = 0
        for entity, attributes in dummy_entity_attributes_map.items():
            sum = sum + len(attributes)
        return sum

    @staticmethod
    def parse_attribute_expression(attribute_expression):
        match = re.search(r"#(\d).(\w*)([+-])(\d)", attribute_expression)
        referenced_entity_id = int(match.group(1))
        referenced_entity_attribute = match.group(2)
        operation = match.group(3)
        offset = int(match.group(4))
        return referenced_entity_id, referenced_entity_attribute, operation, offset

    @staticmethod
    def evaluate_attribute(
        entity_id,
        attr_name,
        attr_value,
        dummy_entity_attributes_map,
        max_passes,
        depth=0,
    ):
        if depth > max_passes:
            logger.error(f"Potential circular reference detected!")
            return attr_value
        if isinstance(attr_value, int):
            return attr_value
        print("*******")
        print(attr_name, attr_value)

        referenced_entity_id, referenced_entity_attribute, operation, offset = Landscape.parse_attribute_expression(
            attr_value
        )
        print(referenced_entity_id, referenced_entity_attribute)
        referenced_entity_attribute_value = dummy_entity_attributes_map[
            referenced_entity_id
        ][referenced_entity_attribute]
        if isinstance(referenced_entity_attribute_value, int):
            if operation == "+":
                val = referenced_entity_attribute_value + offset
            elif operation == "-":
                val = referenced_entity_attribute_value - offset
            else:
                val = referenced_entity_attribute_value
            dummy_entity_attributes_map[entity_id][attr_name] = val
            return val
        else:
            val = Landscape.evaluate_attribute(
                referenced_entity_id,
                referenced_entity_attribute,
                referenced_entity_attribute_value,
                dummy_entity_attributes_map,
                max_passes,
                depth + 1,
            )
            dummy_entity_attributes_map[referenced_entity_id][attr_name] = val
            dummy_entity_attributes_map[entity_id][attr_name] = val
            return val
