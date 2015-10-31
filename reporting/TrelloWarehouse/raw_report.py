# -*- coding: utf-8 -*-

from trello.card import *
import logging
import project


class RawReport(object):
    """The RawReport class reprsents a report structure for the projects report"""
    def __init__(self, _name, _trello, _board_lists):
        """
        :param _name: the name this report
        :param _trello: TrelloClient obj
        :param _board_lists: the tuples of [(board, list)] that must be reported upon
        """
        self.name = _name
        self.trello = _trello
        self.projects = []
        self.board_lists = _board_lists
        self.gen_date = ""
        self.logger = logging.getLogger("sysengreporting")

    def __str__(self):
        return "Report '%s' on '%s' owned by '%s'" % (self.name, self.board_lists)

    def repopulate_projects_list(self):
        self.projects = []
        for (tr_board_id, tr_list_id) in self.board_lists:

            # get board and list to derive projects from
            tr_board = self.trello.get_board(tr_board_id);
            self.logger.debug('Obtained board: %s' % (tr_board.name));
            tr_list = tr_board.get_list(tr_list_id);
            self.logger.debug('Obtained board: %s' % (tr_list.name));

            # get the list of all projects
            for _project in tr_list.list_cards():
                self.logger.debug('Adding project: %s' % (_project.name));
                self.logger.debug('Card id is: %s' % (_project.id));
                self.projects.append(project.Project(_project.id, self.trello));
                self.projects[-1].get_name();
                self.projects[-1].get_tags();
                self.projects[-1].get_status();
                self.projects[-1].get_members();
                self.projects[-1].get_detailed_status();
                

        
