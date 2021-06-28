class SchemaNotRegisteredException(Exception):
    def __init__(self, entity_type):
        self.entity_type = entity_type


class InvalidSyntax(Exception):
    def __init__(self, desc):
        self.desc = desc
