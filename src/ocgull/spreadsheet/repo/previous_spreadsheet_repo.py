import json
import logging

import boto3
import botocore

from ocgull.spreadsheet.spreadsheet import Spreadsheet

logger = logging.getLogger(__name__)


class PreviousSpreadsheetRepo():
    """
    Class to read previously stored sheets information.
    """
    BUCKET_NAME = "ocgull-snapshots"

    def __init__(self, config):
        """
        :param config: The configuration for this repo.
        :type config: RepoConfig.
        """
        self.snapshot_read_filename = config.get_snapshot_read_filename()
        self.snapshot_write_filename = config.get_snapshot_write_filename()

        self.s3 = boto3.resource("s3")

    def fetch(self):
        try:
            obj = self.s3.Object(self.BUCKET_NAME, self.snapshot_read_filename)
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
            obj = self.s3.Object(self.BUCKET_NAME, self.snapshot_write_filename)
            obj.put(
                Body=spreadsheet.dumps(),
                ContentType="application/json",
            )
        except botocore.exceptions.ClientError as e:
            logger.error("Failed saving last snapshot to S3: {}".format(e.response))
        else:
            logger.info("Saved snapshot.")
