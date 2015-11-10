# -*- coding: utf-8 -*-

from trello.card import *
import logging
from . import assignment, report_group_assignments


class AssignmentsReport(object):
    """The AssignmentsReport class reprsents a report structure for the assignments report"""
    def __init__(self, _name, _group_report):
        """
        :param _name: the name this report
        :param _group_report: GroupAssignmentsReport object
        """
        self.name = _name
        self.group_report = _group_report
        self.assignments = []
        self.board_lists = _group_report.board_lists
        self.gen_date = _group_report.gen_date
        self.logger = logging.getLogger("sysengreporting")
        self.full_name = self.name + "-" + self.gen_date;

    def __str__(self):
        return "Report '%s' on '%s' owned by '%s'" % (self.name, self.board_lists)

    def repopulate_report(self):
        self.assignments = []
        line_id = 0
        for g_assignment in self.group_report.group_assignments:
            self.logger.debug('Assignments report on card: %s' % (g_assignment.content['name']))
            if not g_assignment.content['members']:
                self.assignments.append(assignment.Assignment(line_id, g_assignment, ""))
                line_id += 1
                self.logger.debug('no members in the assignment %s' % (g_assignment.content['name']))
            for member in g_assignment.content['members']:
                pg = assignment.Assignment(line_id, g_assignment, member.full_name)
                self.assignments.append(pg)
                self.logger.debug('Assignment member is %s' % (member.full_name))
                line_id += 1

                

        
