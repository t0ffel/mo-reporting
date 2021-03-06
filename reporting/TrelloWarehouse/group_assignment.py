# -*- coding: utf-8 -*-

from trello.card import *
from trello.exceptions import *

import logging
import re

class GroupAssignment(object):
    """The GroupAssignment class reprsents a trello assignment card. The difference from Assignment class is that GroupAssignment may have several members. This is in the context of Systems Design and Engineering"""
    def __init__(self, _id, _trello):
        """
        :param _id: ID of the trello card representing this Project
        :param _trello: TrelloClient object
        """
        self.content = {
            'team' : "", #sub-team within SysEng group
            'name' : '',
            'id'   : _id,
            'members': [],
            'funding_buckets': "",
            'status': "",
            'label': "",
            'last_updated': '',
            'detailed_status': '',
            'short_url': '',
            'board_name': '',
            'list_name': '',
            'tags' : [],
            'latest_move': '',
            'due_date': '',
        }
        self.trello = _trello
        self.logger = logging.getLogger("sysengreporting")
        while True:
            try:
                self._card = self.trello.get_card(self.content['id'])
                self._card.fetch(True); #fetch all card's properties at once
            except ResourceUnavailable as e:
                self.logger.error('Trello unavailable! %s' % (e))
                continue
            break
        self.logger.debug('----GroupAssignment object created----')

    def __str__(self):
        return "GroupAssignment (%s) '%s' owned by '%s'" % (self.content['id'], self.content['name'], self.content['team'])

    def get_name(self):
        self.content['name'] = self._card.name.decode(encoding='UTF-8')

    def get_tags(self, special_tags):
        self.content['tags'] = [];

        for tag_type in special_tags.keys():
            self.content[tag_type] = []

        # obtain all tags
        _all_tags = re.findall('\[.*?\]',(str(self._card.name)))
        _all_tags.extend(re.findall('\[.*?\]', str(self._card.desc)))
        self.logger.debug('all tags: %s' % _all_tags)

        # filter out special tag types, see report.yml for tag types.
        for tag in _all_tags:
            for tag_type in special_tags.keys():
                cur_tag = special_tags[tag_type]; # tag type being currently reviewed
                if tag[1:len(cur_tag[':tag_prefix'])+1] == cur_tag[':tag_prefix']:
                    break
            if tag[1:len(cur_tag[':tag_prefix'])+1] == cur_tag[':tag_prefix']:
                    self.content[tag_type].append(tag[len(cur_tag[':tag_prefix'])+1:-1]) #Special tag gets appended to the respective list
            else:
                self.content['tags'].append(tag); #Other tags go to general tags list

    def get_status(self):
        for label in self._card.labels:
            if label.name == b'Ok':
                self.content['status'] = '3-Ok'
                self.content['label'] = 'success'
                return
            if label.name == b'Issues':
                self.content['status'] = '2-issues'
                self.content['label'] = 'warning';
                return;
            if label.name == b'Blocked':
                self.content['status'] =  '1-Blocked';
                self.content['label'] = 'danger';
                return;
            self.content['status'] = '0-n/a';
            self.content['label'] = 'default';
            return;

    def get_members(self):
        self.content['members'] = [];
        for _member_id in self._card.member_id:
            while True:
                try:
                    self.content['members'].append(self.trello.get_member(_member_id))
                except ResourceUnavailable as e:
                    self.logger.debug('Trello unavailable! %s' % (e))
                    continue
                break
            self.logger.debug('Adding members %s to the card %s' % (self.content['members'][-1].full_name, self.content['name']));

    def get_detailed_status(self):
        while True:
            try:
                self._card.fetch_actions('updateCard:idList')
            except ResourceUnavailable as e:
                self.logger.error('Trello unavailable! %s' % (e))
                continue
            break
        self.logger.debug('comments: %s' % (self._card.comments))
        if self._card.comments != []:
            self.content['detailed_status'] = self._card.comments[-1]['data']['text'];
        else:
            self.content['detailed_status'] = 'n/a'
        self.content['last_updated'] = self._card.dateLastActivity.strftime("%Y-%m-%d %H:%M");
        self.logger.debug('Detailed Status: %s' % (self.content['detailed_status']));
        self.logger.debug('Last Updated: %s' % (self.content['last_updated']));
        try:
            self.content['latest_move']=self._card.latestCardMove_date.strftime("%Y-%m-%d %H:%M");
        except IndexError:
            self.content['latest_move']='';
        self.content['due_date'] = self._card.due_date;

    def get_url(self):
        self.content['short_url'] = self._card.url

    def get_board_list(self, _board, _list):
        self.content['board_name'] = _board.decode(encoding='UTF-8')
        self.content['list_name'] = _list.decode(encoding='UTF-8')

