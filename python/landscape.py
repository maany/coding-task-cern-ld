import logging
import re

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
    def __check_attribute_type(attributes, entity):
        additional_attributes = []
        invalid_type_attributes = []
        entity_type = entity['type']
        if entity_type not in Landscape.registered_entity_schemas.keys():
            raise SchemaNotRegisteredException(entity_type=entity_type)
        schema = Landscape.registered_entity_schemas[entity_type]
        for attribute, val in attributes.items():
            try:
                schema[attribute](val)
            except (TypeError, ValueError) as e:
                logger.warning(f"Value supplied for attribute {attribute} of {entity_type} is incompatible "
                               f"with {schema[attribute]}")
                invalid_type_attributes.append(attribute)
            except KeyError as e:
                logger.warning(f"Addition attribute {attribute} of entity {entity_type} will be ignored")
                additional_attributes.append(attribute)
        return additional_attributes, invalid_type_attributes

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
                regular_attrs[attr_and_val[0]] = int(attr_and_val[1])
            else:
                logger.warning(f"Syntax error in line representing attribute {attribute} of {dummy_entity}.")
                invalid_attrs.append(attribute)

        dummy_entity['regular_attrs'] = regular_attrs
        dummy_entity['expression_attrs'] = expression_attrs

        if len(invalid_attrs) > 0:
            raise InvalidSyntax(f'Could not parse the following attributes: {invalid_attrs}')

    def __parse_entity(self, entity):
        entity_info = entity.split("\n")
        entity_type = entity_info[0]

        if entity_info[1].startswith('#'):
            entity_id = int(entity_info[1][1:])
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
            additional_parameters, invalid_parameters = self.__check_attribute_type(
                attributes=dummy_entity['regular_attrs'], entity=dummy_entity)
            final_regular_attrs = [attr for attr in dummy_entity['regular_attrs'] if
                                   attr not in additional_parameters or attr not in invalid_parameters]
            dummy_entity['final_regular_attrs'] = final_regular_attrs
        except SchemaNotRegisteredException as ex:
            logger.error(f"Could not correctly parse attributes of {dummy_entity['type']} due to missing schema")
        except InvalidSyntax:
            logger.error(f"syntax errors detected in {entity}")
        finally:
            return entity_id, dummy_entity

    def __search_by_entity_id(self, entity_id, list_of_dicts):
        result = [the_dict for the_dict in list_of_dicts if entity_id in list(the_dict.keys())]
        if len(result) > 0:
            return result[0]
        else:
            return None

    def __evaluate_expression(self, entity_id, attribute_name, expression, all_entity_ids, all_expression_attrs,
                              all_regular_attrs,
                              count=0):
        if count > len(all_expression_attrs):
            return None  # possible cyclic reference

        match = re.search("#(\d).(\w*)([+-])(\d)", expression)
        referenced_entity_id = int(match.group(1))
        referenced_entity_attribute = match.group(2)
        operation = match.group(3)
        offset = int(match.group(4))

        # check id exists continue, else return None and throw warning
        if referenced_entity_id not in all_entity_ids:
            logger.warning(f"Entity with id {referenced_entity_id} does not exist but has been referenced "
                           f"by #{entity_id}.{attribute_name}")
            return None
        available_attributes = \
            [x[referenced_entity_id] for x in all_regular_attrs if referenced_entity_id in list(x.keys())][0]
        if referenced_entity_attribute in available_attributes:
            value = available_attributes[referenced_entity_attribute]
            if operation == '+':
                return value + offset
            elif operation == '-':
                return value - offset
            else:
                logger.error(f'Cannot identify operation "{operation}" in {expression}')
                return None
            all_regular_attrs[e]
        referenced_entity = self.__search_by_entity_id(referenced_entity_id, all_expression_attrs)
        if referenced_entity is not None:
            pass

    def __evluatate_attributes(self, all_entity_ids, all_expression_attrs, all_regular_attrs, run_count=0):
        for entity_id, expression_attr in all_expression_attrs.items():
                for dependent_attribute, expression in expression_attr.items():
                    result = self.__evaluate_expression(entity_id, dependent_attribute, expression, all_entity_ids,
                                                        all_expression_attrs,
                                                        all_regular_attrs)

                # except Exception:
                #     logger.error("Exception")
                # else:
                #     pass

    def load(self, input):
        entities = input.strip().split("\n\n")
        for entity in entities:
            dummy_entity_id, dummy_entity = self.__parse_entity(entity)
            if dummy_entity_id is not None:
                self.entities_with_id[dummy_entity_id] = dummy_entity
            else:
                self.entities_sans_id.append(dummy_entity)
        all_expression_atts = {entity_id: entity['expression_attrs'] for entity_id, entity in self.entities_with_id.items()}
        all_regular_attrs = {entity_id: entity['regular_attrs'] for entity_id, entity in self.entities_with_id.items() }
        # all_expression_atts = [{entity_id: entity['expression_attrs']} for entity_id, entity in
        #                        self.entities_with_id.items() if len(entity['expression_attrs']) > 0]
        # all_regular_attrs = [{entity_id: entity['regular_attrs']} for entity_id, entity in
        #                      self.entities_with_id.items() if len(entity['regular_attrs']) > 0]
        all_entity_ids = [entity_id for entity_id, entity in self.entities_with_id.items()]
        self.__evluatate_attributes(all_entity_ids, all_expression_atts, all_regular_attrs)
