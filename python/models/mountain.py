from python.models.abstract_entity import AbstractEntity, AbstractEntityMeta


class Mountain(AbstractEntity, metaclass=AbstractEntityMeta):
    def __init__(self, idx):
        super(Mountain, self).__init__(
            idx=idx,
            entity_type="mountain",
            attributes=
                {
                    "left": 0,
                    "right": 0,
                    "center": 0,
                    "height": 0
                }
        )
