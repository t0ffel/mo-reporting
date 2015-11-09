# -*- coding: utf-8 -*-

import os
import csv

from trello import TrelloClient
import logging

import httplib2

from . import raw_report, project, assignment, granular_report
from .exporter import gwriter

class TrelloWarehouse(object):
    """
    Class representing all Trello information required to do the SysDesEng reporting.
    """

    def __init__(self):
        self.logger = logging.getLogger("sysengreporting")
        self.client = TrelloClient(api_key = os.environ['TRELLO_API_KEY'],
                                   api_secret = os.environ['TRELLO_API_SECRET'],
                                   token = os.environ['TRELLO_TOKEN'],
                                   token_secret = os.environ['TRELLO_TOKEN_SECRET'])
        syseng_board_id = '55b8e03be0b7b68131139cf1'; #Real syseng board
        inprogress_list_id = '55b8e064fb3f1d621db0746f'; #real syseng in progress list
        #syseng_board_id = '562e7903530bf0e9c3101ba8' #SysDesEng board
        #inprogress_list_id = '562e79cf28eca88fa48eebe8' #list with 2 projects
        self.raw_report = raw_report.RawReport("syseng report", self.client, [(syseng_board_id, inprogress_list_id)]);
        self.raw_report.repopulate_projects_list();

        self.gran_report = granular_report.GranularReport("granular report", self.raw_report)
        self.gran_report.repopulate_report();
        self.gSCOPES = "https://www.googleapis.com/auth/drive " + "https://spreadsheets.google.com/feeds/"
        self. gCLIENT_SECRET_FILE = 'client_secret.json'
        self.gAPPLICATION_NAME = 'gDrive Trello Warehouse'

    def _get_title(self, short_url_id):
        return "UNKNOWN" # TODO get titel of card identified by short_url_id

    def _add_project(self, project):
        pass

    def _add_assignment(self, assignment):
        pass

    def get_projects(self):
        self.projects.clear()

        # check if there are some SysDesEng projects at all
        if self.sysdeseng_projects_cards is not None:
            # and for each project
            for _project in self.sysdeseng_projects_cards:
                self.logger.debug('fetching card: %s' % (_project.name))
                _project.fetch(True) # get the details from trello.com

                _p = project.Project('Systems Engineering', _project.name, _project.id  )
                self.projects[_project.id] = _p

                self.logger.debug('new project: %s' % str(_p))

                # if the project's card has a checklist
                if _project.checklists is not None:
                    # it is per definition, the list of assignments
                    for item in _project.checklists[0].items:
                        try: # lets try to convert it into an Assignment
                            _aid = item['name'].split('/')[4]
                            self.assignments[_aid] = assignment.Assignment(_aid, self._get_title(item['name']), _p)

                            self.logger.debug("new assignment %s" % str(self.assignments[_aid]))
                        except IndexError: # if there is no URL in there...
                            self.logger.warning("Assignment '%s' did not link back to a trello card." % (item['name']))
                            pass
        else:
            self.logger.error('sysdeseng_projects_cards was None')

        return self.projects

    def get_all_assignment_ids(self):
        """function returns a list of IDs of all assignments"""

        return self.assignments.keys()

    def get_unrelated_assignments(self):
        """function to filter out any assignment that is not related to a project"""

        _assignments = []
        result = dict()

        all_known_assignments = self.get_all_assignment_ids()

        # lets find the SysEng 'In Progress' list and all its cards
        self.logger.debug('adding SysEng assignments')
        for list in self.syseng_assignments.all_lists():
            if list.name == 'In Progress'.encode('utf-8'):
                _assignments = _assignments + self.syseng_assignments.get_list(list.id).list_cards()

        # and append the E2E 'In Progress' list's cards
        self.logger.debug('adding E2E assignments')
        for list in self.e2e_board.all_lists():
            if list.name == 'In Progress'.encode('utf-8'):
                _assignments = _assignments + self.syseng_assignments.get_list(list.id).list_cards()

        # and get all cards aka assignments
        for _assignment in _assignments:
            _aid = _assignment.url.split('/')[4]
            if _aid in all_known_assignments:
                self.logger.info("we have had assignment '%s' within project '%s'" % (_aid, self.assignments[_aid].project))
            else:
                result[_aid] = assignment.Assignment(_aid, _assignment.name, None)

                self.logger.debug('unrelated assignment: %s' % str(result[_aid]))

        return result

    def get_assignments(self, project_id):
        _assignments = []

        try:
            _assignments = self.projects[project_id].assignments
        except KeyError as e:
            raise

        return _assignments

    def get_assignments0(self, team_name):
        """Return a dict() of SysEng assignments."""

        _cards = []
        _assignments = dict()

        if team_name == 'SysEng':
            for list in self.syseng_assignments.all_lists():
                if list.name == 'In Progress'.encode('utf-8'):
                    _cards = self.syseng_assignments.get_list(list.id).list_cards()

            _assignments[_card.id] = assignment.Assignment(_card.id, _card.name, None, _status = _label)

        return _assignments

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
        writer = gwriter.GWriter(self.gran_report.full_name)
        writer.write_data(self.gran_report.line_items)

