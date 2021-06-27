from python.models.abstract_entity import AbstractEntity, AbstractEntityMeta


class Mountain(AbstractEntity, metaclass=AbstractEntityMeta):
    def __init__(self, idx):
        super(Mountain, self).__init__(
            idx=idx,
            attributes=
                {
                    "left": 0,
                    "right": 0,
                    "height": 0
                }
        )
