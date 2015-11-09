# -*- coding: utf-8 -*-

import gspread

import logging
import os
import httplib2

import oauth2client
from apiclient import errors
from apiclient import discovery
from oauth2client import client
from oauth2client import tools

class GWriter(object):
    """
    Class representing writing reporting data to google sheets via gspread.
    """

    def __init__(self, report_name):
        self.logger = logging.getLogger("sysengreporting")
        #syseng_board_id = '55b8e03be0b7b68131139cf1'; #Real syseng board
        #inprogress_list_id = '55b8e064fb3f1d621db0746f'; #real syseng in progress list

        self.gSCOPES = "https://www.googleapis.com/auth/drive " + "https://spreadsheets.google.com/feeds/"
        self. gCLIENT_SECRET_FILE = 'client_secret.json'
        self.gAPPLICATION_NAME = 'gDrive Trello Warehouse'

        self.credentials = self.g_authenticate();
        self.gc = gspread.authorize(self.credentials)

        http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('drive', 'v2', http=http)

        #self.list_files();

        #self.tmp = self.gc.open_by_key('1U9n7Onrx48azTxInuWOQN5fBHXuFGxYToOlPpRiHo5o')
        self._create_new(report_name)
        self.wks = self.gc.open(report_name).sheet1

        # Need to create the spreadsheet first!

        # Need to open the spread sheet and select worksheet


    def write_data(self, lines):
        """
        Iterate through all the rows/columns and write the actual data
        """
        self.wks.insert_row([ "Project ID", "Project" , "Owner" , "Funding Buckets", "Status" , "Last Updated", "Detailed Status", "Tags"])
        i = 2; # row index
        for line in lines:
            self.wks.insert_row([line.id, line.name, line.member, line.funding_buckets, line.status, line.last_updated, line.detailed_status, line.tags], i);
            i += 1;

    def write_metadata(self):
        """
        Write name/date of the report.. to 2nd worksheet?
        write 1st row here as well.
        """
        self.wks.insert_row([ "Project ID", "Project" , "Owner" , "Funding Buckets", "Status" , "Last Updated", "Detailed Status", "Tags"])

    def csv_write(self, _dir_path):
        csv_file = open(os.path.join(_dir_path, self.gran_report.full_name + '.csv'),'w+');
        csv_writer = csv.writer(csv_file);
        csv_writer.writerow(["Owner", "Title", "Status", "Tags", "Funding Bucket", "Detailed Status", "Last Updated"]);
        for line in self.gran_report.line_items:
            csv_writer.writerow([line.member, line.name, line.status, line.tags, line.funding_buckets, line.detailed_status, line.last_updated]);
        csv_file.close();

    def g_authenticate(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                   'drive-python-credentials.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.gCLIENT_SECRET_FILE, self.gSCOPES)
            flow.user_agent = self.gAPPLICATION_NAME
            flags = tools.argparser.parse_args(args=["--noauth_local_webserver"])
            credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)
        self.logger.debug("Authenticated to Google Drive!")
        return credentials

    def insert_file(self, service, title, description, mime_type, filename):
        """Insert new file.

        Args:
          service: Drive API service instance.
          title: Title of the file to insert, including the extension.
          description: Description of the file to insert.
          parent_id: Parent folder's ID.
          mime_type: MIME type of the file to insert.
          filename: Filename of the file to insert.
        Returns:
          Inserted file metadata if successful, None otherwise.
        """
        media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
        body = {
            'title': title,
            'description': description,
            'mimeType': mime_type,
    #        'parent' : '0Bz-unW9GjAeIMjJBWVR2eWFBQUk', # reports folder
            'convert': True,
        }
        self.logger.debug('Upload metadata: %s' % (body))

        try:
            file = service.files().insert(
                body=body,
                media_body=media_body).execute()

            return file
        except errors.HttpError as error:
            self.logger.error('An error occured: %s' % error)


    def list_files(self):
            http = self.credentials.authorize(httplib2.Http())
            service = discovery.build('drive', 'v2', http=http)

            results = service.files().list(maxResults=10).execute()
            items = results.get('items', [])
            if not items:
                self.logger.debug('No files found.')
            else:
                self.logger.debug('Files:')
                for item in items:
                    self.logger.debug('{0} ({1})'.format(item['title'], item['id']))


    def _create_new(self,
                            target_name=None,
                            folder=None,
                            sheet_description="new"):
        if target_name is None:
            raise KeyError("Must specify a name for the new document")

        body = {'title': target_name }
        if folder:
            body['parents'] = [{'kind' : 'drive#parentReference',
                                'id' : folder['id'],
                                'isRoot' : False }]

        drive_service = self.service

            # Create new blank spreadsheet.
        self.logger.debug("Creating blank spreadsheet.")

        body['mimeType'] = 'application/vnd.google-apps.spreadsheet'
        try:
            new_document = drive_service.files().insert(body=body).execute()
        except Exception as e:
            self.logger.exception("gdata API error. %s", e)
            raise e

        self.logger.info("Created %s spreadsheet with ID '%s'",
                sheet_description,
                new_document.get('id'))

        return new_document

