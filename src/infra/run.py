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

def _factory(env, notify_via_email):
    gcp_api_key = os.environ.get('GCP_API_KEY')

    if env == 'prod':
        repoconfig = RepoConfig(Environment.PROD)
    elif env == 'dev':
        repoconfig = RepoConfig(Environment.DEV)
    else:
        raise ValueError("Unknown environment: {}".format(env))

    notifier = EmailNotifier() if notify_via_email else PrintNotifier()

    gull = OcGull(SpreadsheetRepo(repoconfig, gcp_api_key),
            PreviousSpreadsheetRepo(repoconfig), notifier)

    return gull


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

    gull = _factory('dev', notify_via_email=True)
    print(gull.pull())
