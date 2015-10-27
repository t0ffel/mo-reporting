# -*- coding: utf-8 -*-

from trello.card import *

class Assignment(object):
    """The Assignment class reprsents an Assignment of a Person to a Project"""
    def __init__(self, _id, _project):
        """
        :param _id: ID of the trello card representing this Assignment
        :param _project: the Project this assignment belongs to
        """
        self.id = _id
        self.project = _project

    def __str__(self):
        return "Assignment (%s) for Project '%s'" % (self.id, self.project.name)
