import copy

from landscape import Landscape

class EntityMeta(type):
    created_entities = {}

    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        EntityMeta.append_is_attrs(cls, name)
        EntityMeta.register_loader_and_schema(cls, name, dict)

    def append_is_attrs(cls, name):
        for (
            existing_entity_name,
            existing_entity_cls,
        ) in EntityMeta.created_entities.items():
            attribute = f"is_{existing_entity_name}"
            current_attribute = f"is_{name.lower()}"
            setattr(cls, attribute, False)
            setattr(existing_entity_cls, current_attribute, False)

        EntityMeta.created_entities[name.lower()] = cls
        setattr(cls, f"is_{name.lower()}", True)
        setattr(cls, "type", name)

    def register_loader_and_schema(cls, name, dict):
        cls_path = f'{dict["__module__"]}.{dict["__qualname__"]}'
        if "unicode_8_bit" not in dict:
            raise ValueError(
                f"Please specify an class variable of type string `unicode_8_bit` in {cls_path}"
                f"This value is used to find objects of type {name} while parsing input data."
            )

        if "load" not in dict:
            raise ValueError(
                f"Please specify a classmethod `load(str_repr: str) -> {cls_path}` in {cls_path}. "
                f"This function is used to generate objects of type {name} while parsing input data."
            )

        if "default_attribute_map" not in dict:
            raise ValueError(
                f"In {cls_path}, please specify a classmethod default_attribute_map() -> dict that returns a "
                f"dictionary [T] of schema -> T[attribute_name] = default_attribute_value"
            )

        Landscape.registered_loaders[cls.unicode_8_bit] = cls.load
        Landscape.registered_entity_schemas[
            cls.unicode_8_bit
        ] = cls.default_attribute_map


class AbstractEntity:
    """
    A class to represent entities in a landscape
    """

    def __init__(self, attributes: dict, idx=None):
        custom_attributes = copy.deepcopy(attributes)
        self._attribute_dict = attributes
        self._custom_attributes = custom_attributes
        self._id = idx
        self._type = None
        self._attribute_type_map = None

        for attribute, default_value in custom_attributes.items():
            setattr(self, attribute, default_value)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self._attribute_dict[key] = value

    def __getitem__(self, item):
        return self._attribute_dict[item]

    def __str__(self):
        all_data = [f"ID: {self.id}", f"type: {self.entity_type}"]
        all_data.extend(
            [f"{attribute}: {self[attribute]}" for attribute in self.custom_attributes]
        )
        return "\n".join(all_data)

    @property
    def custom_attributes(self):
        return self._custom_attributes

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, idx):
        self._id = idx

    @property
    def entity_type(self):
        if self._type is None:
            self._type = self.__class__.__name__
        return self._type

    @staticmethod
    def generate_attribute_type_map(default_attributes: dict) -> dict:
        attribute_types = {
            attribute: type(value) for attribute, value in default_attributes.items()
        }
        return attribute_types

    def set_attribute(self, attribute, value):
        setattr(self, attribute, value)
