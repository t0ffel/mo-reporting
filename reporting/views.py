# -*- coding: utf-8 -*-

import logging

from django.shortcuts import render

from TrelloWarehouse import trello_warehouse, assignment


logger = logging.getLogger(__name__)

warehouse = trello_warehouse.TrelloWarehouse()

def index(request):
    context = { 'mynameis': 'Christoph Görn' }

    return render(request, 'reporting/index.html', context)

def get_unrelated_assignments(request):
    unrelated_assignments = warehouse.get_unrelated_assignments()

    for aid, assignment in unrelated_assignments.iteritems():
        print aid, ' is ', str(assignment)

    unrelated_assignments_len = 0

    if unrelated_assignments is not None:
        unrelated_assignments_len = len(unrelated_assignments)

    context = {
        'all_unrelated_assignments': unrelated_assignments,
        'total_num_unrelated_assignments': unrelated_assignments_len
    }

    return render(request, 'reporting/unrelated.html', context)

def get_current_projects(request):
    all_projects = warehouse.get_projects()

    context = {
        'all_projects': all_projects
    }

    return render(request, 'reporting/projects.html', context)

def get_assignments(request, project_id):
    context = {
        'assignments': warehouse.get_assignments(project_id)
    }

    return render(request, 'reporting/assignments.html', context)
