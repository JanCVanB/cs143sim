"""This module contains all error definitions.

.. autosummary:

    InputFileSyntaxError
    InputFileUnknownError
    MissingAttribute

.. moduleauthor:: Samuel Richerd <dondiego152@gmail.com>
.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""


class InputFileSyntaxError(Exception):
    """InputFileSyntaxError is an `Exception` thrown when an unrecognized syntax
    is used in the input file.
    """
    def __init__(self, line_number, message):
        self.line_number = line_number
        self.message = message

    def __str__(self):
        return 'Input File Syntax Error: (Line ' + str(self.line_number) + ') ' + self.message


class InputFileUnknownReference(Exception):
    """InputFileUnknownReference is an `Exception` thrown when a link or host makes reference
    to an unknown object (Host/Router/Link)
    """
    def __init__(self, line_number, message):
        self.line_number = line_number
        self.message = message

    def __str__(self):
        return 'InputFileUnknownReference (Line ' + str(self.line_number) + '): ' + self.message


class MissingAttribute(Exception):
    """MissingAttribute is an `Exception` designed to notify the user that the
    input file is missing information
    """
    def __init__(self, obj_type, obj_id, missing_attr):
        self.obj_type = obj_type
        self.obj_id = obj_id
        self.missing_attr = missing_attr

    def __str__(self):
        return 'I/O Error: Type ' + self.obj_type + ' (ID: ' + self.obj_id + \
               ') is missing attribute ' + self.missing_attr
