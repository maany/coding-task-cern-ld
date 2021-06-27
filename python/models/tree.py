from python.models.abstract_entity import AbstractEntity, AbstractEntityMeta


class Tree(AbstractEntity, metaclass=AbstractEntityMeta):

    def __init__(self, idx=None):
        super().__init__(
            idx=idx,
            attributes=
            {
                "center": 0,
                "height": 0
            }
        )
