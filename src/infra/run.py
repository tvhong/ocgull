#!/usr/bin/env python

import getopt
import json
import logging
import os
import sys

from ocgull import DataSource, OcgullFactory

logger = logging.getLogger(__name__)


def _config_root_logger_for_aws():
    """
    AWS lambda calls logging.basicConfig themselves. We want to override this.
    """
    root = logging.getLogger()
    for handler in root.handlers or []:
        root.removeHandler(handler)

    logging.basicConfig(level=logging.INFO)


def handle_aws_lambda_event(event, context):
    _config_root_logger_for_aws()

    gcp_api_key = os.environ['GCP_API_KEY']
    datasource = DataSource.PROD if event['prod'] == True else DataSource.TEST
    notify_via_email = event['email'] == True
    email_addresses = (os.environ['OCGULL_EMAILS'].split(',') if notify_via_email
            else None)

    gull = OcgullFactory.create(gcp_api_key, datasource, email_addresses)

    return {
        'statusCode': 200,
        'body': json.dumps([(sheet.id, sheet.title, sheet.protection) for sheet in gull.pull()])
    }


if __name__ == '__main__':
    HELP_TEXT = 'Usage: run.py [-p] [-e <email1>,<email2>]'

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hpe:', ['prod', 'emails='])
    except getopt.GetoptError as err:
        print(err)
        print(HELP_TEXT)
        sys.exit(2)

    datasource = DataSource.TEST
    email_addresses = []
    for option, argument in opts:
        if option in ('-h', '--help'):
            print(HELP_TEXT)
            sys.exit()
        elif option in ('-p', '--prod'):
            datasource = DataSource.PROD
        elif option in ('-e', '--emails'):
            email_addresses = argument.split(',')

    gcp_api_key = os.environ['GCP_API_KEY']
    gull = OcgullFactory.create(gcp_api_key, datasource, email_addresses)

    gull.pull()
