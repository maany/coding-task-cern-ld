import copy


class AbstractEntityMeta(type):
    created_entities = {}

    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        for existing_entity_name, existing_entity_cls in AbstractEntityMeta.created_entities.items():
            attribute = f"is_{existing_entity_name}"
            current_attribute = f"is_{name.lower()}"
            setattr(cls, attribute, False)
            setattr(existing_entity_cls, current_attribute, False)

        AbstractEntityMeta.created_entities[name.lower()] = cls
        setattr(cls, f"is_{name.lower()}", True)
        setattr(cls, "type", name)


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

        for attribute, default_value in custom_attributes.items():
            setattr(self, attribute, default_value)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self._attribute_dict[key] = value

    def __getitem__(self, item):
        return self._attribute_dict[item]

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

    def __str__(self):
        all_data = [f"ID: {self.id}", f"type: {self.entity_type}"]
        all_data.extend(
            [f"{attribute}: {self[attribute]}" for attribute in self.custom_attributes])
        return "\n".join(all_data)
