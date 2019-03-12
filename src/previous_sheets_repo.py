import json
import logging

import boto3
import botocore

from sheet import Sheet

logger = logging.getLogger(__name__)


class PreviousSheetsRepo():
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
            data = []

        return [Sheet.from_dict(d) for d in data]

    def save_snapshot(self, sheets):
        """
        Save the last snapshot to storage.
        """
        data = [sheet.to_dict() for sheet in sheets]
        try:
            obj = self.s3.Object(self.BUCKET_NAME, self.LAST_SNAPSHOT_WRITE)
            obj.put(
                Body=json.dumps(data),
                ContentType="application/json",
            )
        except botocore.exceptions.ClientError as e:
            logger.error("Failed saving last snapshot to S3: {}".format(e.response))
