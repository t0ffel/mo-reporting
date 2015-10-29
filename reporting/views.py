# -*- coding: utf-8 -*-

import logging

from django.shortcuts import render

from reporting.TrelloWarehouse import trello_warehouse, assignment


logger = logging.getLogger(__name__)

warehouse = trello_warehouse.TrelloWarehouse()

def index(request):
    context = { 'all_syseng_assignments':  warehouse.get_assignments0('SysEng') }

    return render(request, 'reporting/index.html', context)

def get_unrelated_assignments(request):
    unrelated_assignments = warehouse.get_unrelated_assignments()

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
    a = warehouse.get_assignments(project_id)

    print(a)

    context = {
        'assignments': a
    }

    return render(request, 'reporting/assignments.html', context)
