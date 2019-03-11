import json
import logging

import boto3

from sheet import Sheet

logger = logging.getLogger(__name__)


class PreviousSheetsRepo():
    """
    Class to read previously stored sheets information.
    """
    BUCKET_NAME = 'ocgull-snapshots'
    LAST_SNAPSHOT = 'last-snapshot.json'

    def __init__(self):
        self.s3 = boto3.resource('s3')

    def fetch(self):
        try:
            obj = self.s3.Object(self.BUCKET_NAME, self.LAST_SNAPSHOT)
            response = obj.get()
            data = json.loads(response['Body'].read())
        except self.s3.meta.client.exceptions.NoSuchKey:
            logger.info("Last snapshot file does not exist yet.")
            data = []

        return [Sheet.from_dict(d) for d in data]
