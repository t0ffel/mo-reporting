# -*- coding: utf-8 -*-

from trello.card import *
import logging
import re

class ProjectGranular(object):
    """The ProjectGranular class reprsents a Project-member line item in the context of Systems Design and Engineering"""
    def __init__(self, _line_id, _project, _member):
        """
        :param _line_id: ID of the trello card representing this Project
        :param _project: project object
        :param _member: name of the member
        """

        self.line_id = _line_id
        self.project = _project
        self.content = _project.content
        self.content['members'] = _member
        self.assignments = _project.assignments
        self.logger = logging.getLogger("sysengreporting")

    def __str__(self):
        return "Project (%s) '%s' owned by '%s'" % (self.line_id, self.name, self.member)


