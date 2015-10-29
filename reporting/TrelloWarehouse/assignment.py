# -*- coding: utf-8 -*-

import re
from trello.card import *


class Assignment(object):
    """The Assignment class reprsents an Assignment of a Person to a Project"""
    def __init__(self, _id, _title, _project, _owner = '', _status = 'UNKNOWN'):
        """
        :param _id: ID of the trello card representing this Assignment
        :param _title: Title of the trello card representing this Assignment
        :param _project: the Project this assignment belongs to
        """
        self.id = _id
        self.title = _title
        self.project = _project
        self.tags = re.findall('\[(.+?)\]', str(self.title)) # there must be no empty tag!!
        self.owner = _owner
        self.status = _status

    def __str__(self):
        if self.project is None:
            return "Assignment (id: %s) '%s' is UNRELATED, tagged with %s" % (self.id, self.title, ', '.join(str(x) for x in self.tags))

        return "Assignment (id: %s) '%s' for Project '%s', tagged with %s" % (self.id, self.title, self.project.name, ', '.join(str(x) for x in self.tags))

    def tagss(self):
        return ', '.join(str(x) for x in self.tags)
