# -*- coding: utf-8 -*-

from django.shortcuts import render

from TrelloWarehouse import trello_warehouse


def index(request):
    context = { 'mynameis': 'Christoph Görn' }

    return render(request, 'reporting/index.html', context)

def get_unrelated_assignments(request):
    warehouse = trello_warehouse.TrelloWarehouse()

    context = { 'all_unrelated_assignments': warehouse.get_unrelated_assignments() }

    return render(request, 'reporting/unrelated.html', context)
