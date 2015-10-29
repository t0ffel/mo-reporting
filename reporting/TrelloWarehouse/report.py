#!/usr/bin/env python3

import logging
import trello_warehouse


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

    _a = warehouse.get_projects()

    _b = warehouse.get_assignments0('SysEng')

    for aid, assignment in _b.items():
        print(str(assignment))

if __name__ == '__main__':

    main()
