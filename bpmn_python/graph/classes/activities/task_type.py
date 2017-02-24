# coding=utf-8
"""
Class used for representing tTask of BPMN 2.0 graph
"""
from graph.classes.activities.activity_type import Activity


class Task(Activity):
    """
    Class used for representing tTask of BPMN 2.0 graph
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(Task, self).__init__()
