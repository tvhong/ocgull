import boto3
from botocore.exceptions import ClientError

SENDER = "dhsocbot@gmail.com"
RECIPIENT = "shiweistg@gmail.com"

CHARSET = "UTF-8"
SUBJECT = "An OC registration sheet unlocked!"

BODY_TEXT = "\"{}\" OC registration sheet has been unlocked.".format("MAR 1 - MAR 2")
BODY_HTML = """<html>
<head></head>
<body>
  <p>"{}" OC registration sheet has been unlocked.</p>
  <p><a href='https://docs.google.com/spreadsheets/d/1TmNjLpt-nI6Mvj80l2JqltdS1A4ecn-d0AT5Zitv-bw'>2019 OC1 Schedule</a></p>
</body>
</html>
            """.format("MAR 1 - MAR 2")

class EmailNotifier():
    def send_notification(self, unlocked_sheets):
        client = boto3.client('ses')

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
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
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
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
