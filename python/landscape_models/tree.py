from typing import TypeVar, Type
from landscape_model_framework.abstract_entity import AbstractEntity, EntityMeta
from landscape_model_framework.exceptions import LoadingError

# annotation
tree = TypeVar("tree")


class Tree(AbstractEntity, metaclass=EntityMeta):
    unicode_8_bit = "🌳"

    def __init__(self, idx=None):
        super().__init__(idx=idx, attributes=Tree.default_attribute_map())

    @classmethod
    def load(cls: Type[tree], dummy_tree: dict) -> tree:
        if len(dummy_tree["all_attrs"]) < 2:
            raise LoadingError(
                f"Specify both center, altitude for Tree entity {dummy_mountain}."
            )

        tree = None
        if "id" in dummy_tree:
            tree = Tree(dummy_tree["id"])
        else:
            tree = Tree()

        for attribute in tree.custom_attributes:
            if attribute in dummy_tree["all_attrs"]:
                value = dummy_tree["all_attrs"][attribute]
                tree.set_attribute(attribute, value)
        return tree

    @classmethod
    def default_attribute_map(cls):
        return {"center": 0, "altitude": 0}
