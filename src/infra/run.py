import json
import logging
import os
import sys

from ocgull.notifier import EmailNotifier, PrintNotifier
from ocgull.ocgull import OcGull
from ocgull.spreadsheet.repo import (PreviousSpreadsheetRepo, RepoConfig,
                                     SpreadsheetRepo)
from ocgull.spreadsheet.repo.constants import Environment

logger = logging.getLogger(__name__)


def handleLambdaEvent(event, context):
    logging.basicConfig(level=logging.INFO)

    repoconfig = RepoConfig(Environment.PROD)
    api_key = os.environ.get('GCP_API_KEY')
    print("Blah")
    logger.warn("POOP!")
    logger.error("POOP! ERror")
    gull = OcGull(SpreadsheetRepo(repoconfig, api_key),
            PreviousSpreadsheetRepo(repoconfig), PrintNotifier())
    return {
        'statusCode': 200,
        'body': json.dumps([(sheet.id, sheet.title, sheet.protection) for sheet in gull.pull()])
    }


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    repoconfig = RepoConfig(Environment.DEV)
    api_key = sys.argv[1]
    gull = OcGull(SpreadsheetRepo(repoconfig, api_key), PreviousSpreadsheetRepo(repoconfig),
            EmailNotifier())
    print(gull.pull())
