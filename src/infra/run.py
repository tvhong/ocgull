import json
import logging
import os
import sys

from infra.constants import Environment
from ocgull.notifier import EmailNotifier, PrintNotifier
from ocgull.ocgull import OcGull
from ocgull.spreadsheet.repo import (PreviousSpreadsheetRepo, RepoConfig,
                                     SpreadsheetRepo)

logger = logging.getLogger(__name__)


def _config_root_logger():
    """
    AWS lambda calls logging.basicConfig themselves. We want to override this.
    """
    root = logging.getLogger()
    for handler in root.handlers or []:
        root.removeHandler(handler)

    logging.basicConfig(level=logging.INFO)

def handleLambdaEvent(event, context):
    _config_root_logger()

    repoconfig = RepoConfig(Environment.PROD)
    api_key = os.environ.get('GCP_API_KEY')
    gull = OcGull(SpreadsheetRepo(repoconfig, api_key),
            PreviousSpreadsheetRepo(repoconfig), PrintNotifier())

    return {
        'statusCode': 200,
        'body': json.dumps([(sheet.id, sheet.title, sheet.protection) for sheet in gull.pull()])
    }


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    repoconfig = RepoConfig(Environment.DEV)
    api_key = os.environ.get('GCP_API_KEY')
    gull = OcGull(SpreadsheetRepo(repoconfig, api_key), PreviousSpreadsheetRepo(repoconfig),
            EmailNotifier())
    print(gull.pull())
