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
        self.name = _project.name
        self.id = _project.id
        self.member = _member
        self.funding_buckets = _project.funding_buckets
        self.status = _project.status
        self.label = _project.label
        self.last_updated = _project.last_updated
        self.detailed_status = _project.detailed_status
        self.tags = _project.tags
        self.assignments = _project.assignments
        self.logger = logging.getLogger("sysengreporting")

    def __str__(self):
        return "Project (%s) '%s' owned by '%s'" % (self.line_id, self.name, self.member)


