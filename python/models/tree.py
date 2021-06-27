from python.models.abstract_entity import AbstractEntity, AbstractEntityMeta


class Tree(AbstractEntity, metaclass=AbstractEntityMeta):

    def __init__(self, idx):
        super().__init__(
            idx=idx,
            entity_type="tree",
            attributes=
            {
                "center": 0,
                "height": 0
            }
        )
