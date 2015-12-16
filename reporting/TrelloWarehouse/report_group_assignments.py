# -*- coding: utf-8 -*-

from trello.card import *
import logging
import datetime
from trello.exceptions import *

from . import group_assignment


class GroupAssignmentsReport(object):
    """The GroupAssignmentReport is a helper class represents a report structure for the assignments report where 1 line corresponds to 1 card"""
    def __init__(self, _name, _trello, _board_lists, _special_tags):
        """
        :param _name: the name this report
        :param _trello: TrelloClient obj
        :param _board_lists: the tuples of [(board, list)] that must be reported upon
        """
        self.name = _name
        self.trello = _trello
        self.group_assignments = []
        self.board_lists = _board_lists
        self.gen_date = datetime.datetime.now().strftime("%Y-%m-%d.%H:%M")
        self.logger = logging.getLogger("sysengreporting")
        self.full_name = self.name + "-" + self.gen_date
        self.special_tags = _special_tags

    def __str__(self):
        return "Report '%s' on '%s' owned by '%s'" % (self.name, self.board_lists)

    def repopulate_report(self):
        self.group_assignments = []
        for (tr_board_id, tr_list_id) in self.board_lists:

            # get board and list to derive projects from
            try:
                tr_board = self.trello.get_board(tr_board_id);
            except Unauthorized as e:
                self.logger.error('Unauthorized to use this Trello board: %s. Error: %s' % (tr_board_id,e))
                return False;
            self.logger.debug('Obtained board: %s' % (tr_board.name));
            tr_list = tr_board.get_list(tr_list_id);
            self.logger.debug('Obtained board: %s' % (tr_list.name));

            # get the list of all projects
            for _g_assignment in tr_list.list_cards():
                self.logger.debug('Adding Group Assignment: %s' % (_g_assignment.name));
                self.logger.debug('Card id is: %s' % (_g_assignment.id));
                self.group_assignments.append(group_assignment.GroupAssignment(_g_assignment.id, self.trello));
                self.group_assignments[-1].get_name();
                self.group_assignments[-1].get_tags(self.special_tags);
                self.group_assignments[-1].get_status();
                self.group_assignments[-1].get_members();
                self.group_assignments[-1].get_detailed_status();
                self.group_assignments[-1].get_url();
                self.group_assignments[-1].get_board_list(tr_board.name, tr_list.name);                
        return True
        
