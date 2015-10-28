# -*- coding: utf-8 -*-

from trello.card import *

class Assignment(object):
    """The Assignment class reprsents an Assignment of a Person to a Project"""
    def __init__(self, _id, _title, _project):
        """
        :param _id: ID of the trello card representing this Assignment
        :param _title: Title of the trello card representing this Assignment
        :param _project: the Project this assignment belongs to
        """
        self.id = _id
        self.title = _title
        self.project = _project

    def __str__(self):
        if self.project is None:
            return "Assignment (%s) '%s' is UNRELATED" % (self.id, self.title)

        return "Assignment (%s) '%s' for Project '%s'" % (self.id, self.title, self.project.name)
