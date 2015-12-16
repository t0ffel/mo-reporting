#!/usr/bin/env python3

from TrelloWarehouse import trello_warehouse
import logging
import tempfile
import os
import yaml

import httplib2
from apiclient import discovery

def main():
    logger = logging.getLogger("sysengreporting")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    _stdlog = logging.StreamHandler()
    _stdlog.setLevel(logging.DEBUG)
    _stdlog.setFormatter(formatter)

    logger.addHandler(_stdlog)


    with open("config/report.yml", 'r') as stream:
        report_config = yaml.load(stream)

    warehouse = trello_warehouse.TrelloWarehouse(report_config[':trello_sources'], report_config[':tags'])
    logger.info('Welcome to the Warehouse!')


    
    if not warehouse.get_granular_report():
        return False
    warehouse.write_gspreadsheet()

if __name__ == '__main__':

    main()
