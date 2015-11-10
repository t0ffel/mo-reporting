# -*- coding: utf-8 -*-

from trello.card import *
import logging
import re

class Assignment(object):
    """The Assignment class represents individual person's task. It is a line item in the Systems Design and Engineering assignments report"""
    def __init__(self, _line_id, _g_assignment, _member):
        """
        :param _line_id: ID of the trello card representing this Project
        :param _g_assignment: GroupAssignment object
        :param _member: name of the member
        """

        self.line_id = _line_id
        self.group_assignment = _g_assignment
        self.content = _g_assignment.content.copy()
        self.content['members'] = _member
        self.logger = logging.getLogger("sysengreporting")

    def __str__(self):
        return "Assignment (%s) '%s' owned by '%s'" % (self.line_id, self.content['name'], self.content['members'])


