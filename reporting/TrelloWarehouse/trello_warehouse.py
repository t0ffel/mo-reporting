# -*- coding: utf-8 -*-

import os
import csv

from trello import TrelloClient
import logging

import httplib2

from . import group_assignment, report_group_assignments, assignment, report_assignments
from .exporter import gwriter

class TrelloWarehouse(object):
    """
    Class representing all Trello information required to do the SysDesEng reporting.
    """

    def __init__(self, report_config, trello_secret):
        self.logger = logging.getLogger("sysengreporting")
        self.client = TrelloClient(api_key = trello_secret[':consumer_key'],
                                   api_secret = trello_secret[':consumer_secret'],
                                   token = trello_secret[':oauth_token'],
                                   token_secret = trello_secret[':oauth_token_secret'])

        #Extract report configuration parameters
        trello_sources = report_config[':trello_sources'];
        self.special_tags = report_config[':tags'];
        self.report_parameters = report_config[':report'];

        # Populate the list of (board, lists) tuples on which to report
        self.report_src = []
        for board_t in trello_sources.keys():
            for list_t in trello_sources[board_t][':lists'].keys():
                self.logger.debug("Adding board %s, list %s to the report" % (trello_sources[board_t][':board_id'], trello_sources[board_t][':lists'][list_t]))
                self.report_src.append( (trello_sources[board_t][':board_id'], trello_sources[board_t][':lists'][list_t]) )


    def get_granular_report(self):
        self.group_report = report_group_assignments.GroupAssignmentsReport("syseng report", self.client, self.report_src, self.special_tags);
        if not self.group_report.repopulate_report():
            self.logger.error('Failed to populate report from Trello');
            return False;
        self.assignments_report = report_assignments.AssignmentsReport("Assignments Report", self.group_report)
        self.assignments_report.repopulate_report();
        return True;

    def display_projects(self):
        """Retrun array of projects"""
        return self.raw_report.projects;

    def display_granular_report(self):
        "Return detailed report"""
        return self.gran_report.line_items;

    def csv_write(self, _dir_path):
        csv_file = open(os.path.join(_dir_path, self.gran_report.full_name + '.csv'),'w+');
        csv_writer = csv.writer(csv_file);
        csv_writer.writerow(["Owner", "Title", "Status", "Tags", "Funding Bucket", "Detailed Status", "Last Updated"]);
        for line in self.gran_report.line_items:
            csv_writer.writerow([line.member, line.name, line.status, line.tags, line.funding_buckets, line.detailed_status, line.last_updated]);
        csv_file.close();


    def write_gspreadsheet(self):
        writer = gwriter.GWriter(self.assignments_report.full_name, self.report_parameters)
        writer.write_headers(writer.wks_granular);
        writer.write_batch_data(self.assignments_report.assignments, writer.wks_granular)

    def list_boards(self):
        syseng_boards = self.client.list_boards()
        for board in syseng_boards:
            for tlist in board.all_lists():
                self.logger.debug('board name: %s is here, board ID is: %s; list %s is here, list ID is: %s' % (board.name, board.id, tlist.name, tlist.id)) 

    def get_assignment_details(self, assignment_id):
        gassign = group_assignment.GroupAssignment(assignment_id, self.client)
        gassign.get_name()
        gassign.get_members()
        gassign.get_tags();
        gassign.get_status();
        gassign.get_detailed_status();
        logger.debug('latest move is: %s' % self.gassign.content['latest_move'])
        logger.debug('Card content: %s' % self.gassign.content)
