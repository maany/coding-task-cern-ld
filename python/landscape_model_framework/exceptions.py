class SchemaNotRegisteredException(Exception):
    """Raised to indicate that the AbstractEntity subclass required to load an entity was not found.

    Arguments:
        entity_type {str} -- THe input entity type
    """

    def __init__(self, entity_type):
        self.entity_type = entity_type


class LoadingError(Exception):
    """Raised if loaders for registered entities for Landscape do not have sufficient information from parsed input to generate an object.
    Arguments:
        message {str} -- details about the loading issue
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class InvalidSyntax(Exception):
    """ Raised to indicate parsing of input data failed due to non-compliance with syntax requirements

    Arguments:
        desc {str} -- Details of syntax violation
    """

    def __init__(self, desc):
        self.desc = desc
        super().__init__(desc)
