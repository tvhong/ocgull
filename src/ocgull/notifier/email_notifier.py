import logging

import boto3
from botocore.exceptions import ClientError

from ocgull.notifier.base import Notifier

logger = logging.getLogger(__name__)


SENDER = "dhsocbot@gmail.com"
RECIPIENT = "shiweistg@gmail.com"

CHARSET = "UTF-8"
SUBJECT = "An OC registration sheet unlocked!"

BODY_TEXT_TEMPLATE = "OC registration sheet(s) has been unlocked: {sheet_titles}."
BODY_HTML_TEMPLATE = """<html>
<head></head>
<body>
  <p>OC registration sheet(s) has been unlocked: {sheet_titles}.</p>
  <p><a href='https://docs.google.com/spreadsheets/d/1TmNjLpt-nI6Mvj80l2JqltdS1A4ecn-d0AT5Zitv-bw'>2019 OC1 Schedule</a></p>
</body>
</html>
            """

class EmailNotifier(Notifier):
    def send_notification(self, unlocked_sheets):
        client = boto3.client('ses')

        sheet_titles = ', '.join([s.title for s in unlocked_sheets])
        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML_TEMPLATE.format(sheet_titles=sheet_titles),
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT_TEMPLATE.format(sheet_titles=sheet_titles),
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
                # ConfigurationSetName=CONFIGURATION_SET,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            logger.error("Failed sending email: {}".format(e.response['Error']['Message']))
        else:
            logger.info("Sent email notification!", extra={"MessageId": response["MessageId"]})
