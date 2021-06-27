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


class AbstractEntity:
    """
    A class to represent entities in a landscape
    """

    def __init__(self, idx, entity_type, attributes: dict, *args, **kwargs):
        self._attribute_dict = attributes
        self._id = idx
        self._entity_type = entity_type

        # AbstractEntity.add_is_x_attributes(self, entity_type)

        for attribute, default_value in attributes.items():
            setattr(self, attribute, default_value)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self._attribute_dict[key] = value

    def __getitem__(self, item):
        return self._attribute_dict[item]

    @property
    def attributes(self):
        return self._attribute_dict

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, idx):
        if id not in AbstractEntity.used_ids:
            self._id = idx
            AbstractEntity.used_ids.append(idx)

    # @property
    # def type(self):
