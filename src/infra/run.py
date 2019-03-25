import json
import logging
import sys

from ocgull import DataSource, OcgullFactory

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

    datasource = DataSource.PROD if event['prod'] == True else DataSource.TEST
    notify_via_email = event['email'] == True
    gull = OcgullFactory.create(datasource, notify_via_email)

    return {
        'statusCode': 200,
        'body': json.dumps([(sheet.id, sheet.title, sheet.protection) for sheet in gull.pull()])
    }


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    datasource = DataSource.PROD if '--prod' in sys.argv else DataSource.TEST
    notify_via_email = '--email' in sys.argv
    gull = OcgullFactory.create(datasource, notify_via_email)

    gull.pull()
