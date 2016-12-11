# coding=utf-8
"""
Package with BPMNDiagramGraph - graph representation of BPMN diagram
"""


class GridCell:
    """
    Helper class used for Grid cell representation. Contains cell coordinates (row and column) and reference to fow node
    """

    def __init__(self, row, col, node_id):
        self.row = row
        self.col = col
        self.node_id = node_id

    def __str__(self):
        return repr(self.row + " " + self.col + " " + self.node_id)