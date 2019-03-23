import logging
import os

from ocgull.notifier import EmailNotifier, PrintNotifier
from ocgull.ocgull import OcGull
from ocgull.spreadsheet.repo import (PreviousSpreadsheetRepo, RepoConfig,
                                     SpreadsheetRepo)

logger = logging.getLogger(__name__)

class OcGullFactory():
    @classmethod
    def create(cls, datasource, notify_via_email):
        """
        Create an OcGull isinstance.

        :param datasource: The datasource to read from.
        :param notify_via_email: Whether the created instance should send email
                notifications.
        """
        logger.info("Creating OcGull with args: {}".format((datasource, notify_via_email)))

        repoconfig = RepoConfig(datasource)
        gcp_api_key = os.environ.get('GCP_API_KEY')
        notifier = EmailNotifier() if notify_via_email else PrintNotifier()

        gull = OcGull(SpreadsheetRepo(repoconfig, gcp_api_key),
                PreviousSpreadsheetRepo(repoconfig), notifier)

        return gull
