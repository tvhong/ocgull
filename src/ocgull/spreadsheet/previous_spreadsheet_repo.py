import json
import logging

import boto3
import botocore

from spreadsheet.spreadsheet import Spreadsheet

logger = logging.getLogger(__name__)


class PreviousSpreadsheetRepo():
    """
    Class to read previously stored sheets information.
    """
    BUCKET_NAME = "ocgull-snapshots"
    LAST_SNAPSHOT_READ = "last-snapshot.json"
    LAST_SNAPSHOT_WRITE = "last-snapshot-fake.json"

    def __init__(self):
        self.s3 = boto3.resource("s3")

    def fetch(self):
        try:
            obj = self.s3.Object(self.BUCKET_NAME, self.LAST_SNAPSHOT_READ)
            response = obj.get()
            data = json.loads(response["Body"].read())
        except self.s3.meta.client.exceptions.NoSuchKey:
            logger.info("Last snapshot file does not exist yet.")
            data = {}

        logger.info("Fetched previous sheets", extra={"gspreadsheet": data})

        try:
            spreadsheet = Spreadsheet(data)
        except ValueError:
            spreadsheet = Spreadsheet({})

        return spreadsheet

    def save_snapshot(self, spreadsheet):
        """
        Save the last snapshot to storage.
        """
        try:
            obj = self.s3.Object(self.BUCKET_NAME, self.LAST_SNAPSHOT_WRITE)
            obj.put(
                Body=spreadsheet.dumps(),
                ContentType="application/json",
            )
        except botocore.exceptions.ClientError as e:
            logger.error("Failed saving last snapshot to S3: {}".format(e.response))
        else:
            logger.info("Saved snapshot.")
