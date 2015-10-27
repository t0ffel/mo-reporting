# -*- coding: utf-8 -*-

from trello.card import *

class Project(object):
    """The Project class reprsents a Project in the context of Systems Design and Engineering"""
    def __init__(self, _team, _name, _id):
        """
        :param _team: the Team name this Project belongs to
        :param _name: the Projects name
        :param _id: ID of the trello card representing this Project
        """

        self.team = _team
        self.name = _name
        self.id = _id
        self.assignments = []

    def __str__(self):
        return "Project (%s) '%s' owned by '%s'" % (self.id, self.name, self.team)

    def add_assignment(self, assignment):
        self.assignments.append(assignment)
