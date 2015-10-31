# -*- coding: utf-8 -*-

from trello.card import *
import logging
import re

class Project(object):
    """The Project class reprsents a Project in the context of Systems Design and Engineering"""
    def __init__(self, _id, _trello):
        """
        :param _id: ID of the trello card representing this Project
        :param _trello: TrelloClient object
        """

        self.team = "SysEng" #unused
        self.name = ""
        self.id = _id # Trello card ID
        self.trello = _trello
        self.members = []
        self.readable_members = ""
        self.funding_buckets = []
        self.status = ""
        self.label = ""
        self.last_updated = ""
        self.detailed_status = ""
        self.tags = []
        self.assignments = []
        self.logger = logging.getLogger("sysengreporting")
        self._card = self.trello.get_card(self.id)
        self._card.fetch(True); #fetch all card's properties at once
        self.logger.debug('----Project object created----')

    def __str__(self):
        return "Project (%s) '%s' owned by '%s'" % (self.id, self.name, self.team)

    def get_name(self):
        self.name = str(self._card.name)

    def add_assignment(self, assignment):
        self.assignments.append(assignment)

    def get_tags(self):
        self.tags = [];
        self.funding_buckets = [];
        # obtain all tags
        _all_tags = re.findall('\[.*?\]',(str(self._card.name)))
        _all_tags.extend(re.findall('\[.*?\]', str(self._card.desc)))
        self.logger.debug('all tags: %s' % _all_tags)

        # filter out special tag types
        for tag in _all_tags:
            if tag[0:4] == '[fb_':
                self.funding_buckets.append(tag[4:-1])
                self.logger.debug('Found fb tag: %s' % (self.funding_buckets[-1]))
                continue;
            self.tags.append(tag);

    def get_status(self):
        for label in self._card.labels:
            if label.name == b'Ok':
                self.status = '3-Ok'
                self.label = 'success'
                return
            if label.name == b'Issues':
                self.status = '2-issues'
                self.label = 'warning';
                return;
            if label.name == b'Blocked':
                self.status =  '1-Blocked';
                self.label = 'danger';
                return;
            self.status = '0-n/a';
            self.label = 'default';
            return;

    def get_members(self):
        self.members = [];
        for _member_id in self._card.member_id:
            self.members.append(self.trello.get_member(_member_id))
            self.logger.debug('Adding members %s to the card %s' % (self.members[-1].full_name, self.name));
            self.readable_members += self.members[-1].full_name + "\n"

    def get_detailed_status(self):
        self.logger.debug('comments: %s' % (self._card.comments))
        if self._card.comments != []:
            self.detailed_status = self._card.comments[-1]['data']['text'];
            self.last_updated = self._card.comments[-1]['date'];
        else:
            self.detailed_status = 'n/a'
            self.last_updated = ''
        self.logger.debug('Detailed Status: %s' % (self.detailed_status));
        self.logger.debug('Last Updated: %s' % (self.last_updated));

