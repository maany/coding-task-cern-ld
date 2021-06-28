class SchemaNotRegisteredException(Exception):
    def __init__(self, entity_type):
        self.entity_type = entity_type


class IncompleteDataException(Exception):
    """Raised if loaders for registered entities for Landscape do not have sufficient information from parsed input to generate an object.
    Arguments:
        message {str} -- details about the missing information
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class InvalidSyntax(Exception):
    def __init__(self, desc):
        self.desc = desc
