class AbstractEntity:
    """
    A class to represent entities in a landscape
    """

    def __init__(self, attributes: dict, *args, **kwargs):
        self._attribute_dict = attributes
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

