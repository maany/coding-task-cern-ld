class AbstractEntityMeta(type):
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        subclasses = cls.__subclasses__()

        property_name = f"is_{name.lower()}"
        setattr(cls, property_name, True)

    def add_is_x_attributes(self, cls):
        subclasses = cls.__subclasses__()

        # property_name = f"is_{entity_type}"
        # if not getattr(cls, property_name, False):
        #     setattr(cls, property_name, False)
        # setattr(instance, property_name, True)


class AbstractEntity(metaclass=AbstractEntityMeta):
    """
    A class to represent entities in a landscape
    """
    used_ids = []

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
