# coding=utf-8
"""
Class including utility method used in diagram importing
"""


class BpmnImportUtils:
    """
    Class including utility method used in diagram importing
    """

    def __init__(self):
        pass

    @staticmethod
    def remove_namespace_from_tag_name(tag_name):
        """
        Helper function, removes namespace annotation from tag name.

        :param tag_name: string with tag name.
        """
        return tag_name.split(':')[-1]

    @staticmethod
    def iterate_elements(parent):
        """
        Helper function that iterates over child Nodes/Elements of parent Node/Element.

        :param parent: object of Element class, representing parent element.
        """
        element = parent.firstChild
        while element is not None:
            yield element
            element = element.nextSibling
