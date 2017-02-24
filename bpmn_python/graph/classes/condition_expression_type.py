# coding=utf-8
"""
Class used for representing condition expression in sequence flow
"""


class ConditionExpression(object):
    """
    Class used for representing condition expression in sequence flow
    Fields:
    - condition: condition expression. Required field. Must be a String.
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(ConditionExpression, self).__init__()
        self.__condition = None

    def get_condition(self):
        """
        Getter for 'condition' field.
        :return:a value of 'condition' field.
        """
        return self.__condition

    def set_condition(self, value):
        """
        Setter for 'condition' field.
        :param value - a new value of 'condition' field. Required field. Must be a String.
        """
        if value is None or not isinstance(value, str):
            raise TypeError("Condition is required and must be set to a String")
        else:
            self.__condition = value
