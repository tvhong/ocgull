import json
import logging
import sys

from ocgull import DataSource, OcGullFactory

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
    gull = OcGullFactory.create(DataSource.PROD, notify_via_email=False)
    return {
        'statusCode': 200,
        'body': json.dumps([(sheet.id, sheet.title, sheet.protection) for sheet in gull.pull()])
    }


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    gull = OcGullFactory.create(DataSource.TEST, notify_via_email=True)
    print(gull.pull())
