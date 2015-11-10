# -*- coding: utf-8 -*-

from trello.card import *
import logging
from . import project_granular, raw_report


class GranularReport(object):
    """The RawReport class reprsents a report structure for the projects report"""
    def __init__(self, _name, _raw_report):
        """
        :param _name: the name this report
        :param _trello: TrelloClient obj
        :param _board_lists: the tuples of [(board, list)] that must be reported upon
        """
        self.name = _name
        self.raw_report = _raw_report
        self.line_items = []
        self.board_lists = _raw_report.board_lists
        self.gen_date = _raw_report.gen_date
        self.logger = logging.getLogger("sysengreporting")
        self.full_name = self.name + "-" + self.gen_date;

    def __str__(self):
        return "Report '%s' on '%s' owned by '%s'" % (self.name, self.board_lists)

    def repopulate_report(self):
        self.line_items = []
        line_id = 0
        for project in self.raw_report.projects:
            self.logger.debug('Granular report on project: %s' % (project.content['name']))
            if not project.content['members']:
                self.line_items.append(project_granular.ProjectGranular(line_id, project, ""))
                line_id += 1
                self.logger.debug('no members in the project %s' % (project.content['name']))
            for member in project.content['members']:
                pg = project_granular.ProjectGranular(line_id, project, member.full_name)
                self.line_items.append(pg)
                self.logger.debug('Project member is %s' % (member.full_name))
                line_id += 1

                

        
