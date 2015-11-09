#!/usr/bin/env python3

from TrelloWarehouse import trello_warehouse
import logging
import tempfile
import os

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

    warehouse = trello_warehouse.TrelloWarehouse()
    logger.info('Welcome to the Warehouse!')

    # save tmp csv file

    # upload tmp file to google drive
#    credentials = warehouse.g_authenticate();
#    http = credentials.authorize(httplib2.Http())
#    service = discovery.build('drive', 'v2', http=http)

#    res = warehouse.insert_file(service, warehouse.gran_report.full_name + '.csv', 'report file', 'text/csv', os.path.join(tmpdir, warehouse.gran_report.full_name + '.csv'))
#    logger.info('Upload status: %s' % (res))    

    warehouse.write_gspreadsheet()

if __name__ == '__main__':

    main()
