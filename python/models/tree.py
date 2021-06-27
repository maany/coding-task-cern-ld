from python.models.abstract_entity import AbstractEntity


class Tree(AbstractEntity):

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
