import logging

from ocgull.notifier import EmailNotifier, PrintNotifier
from ocgull.ocgull import Ocgull
from ocgull.spreadsheet.repo import (PreviousSpreadsheetRepo, RepoConfig,
                                     SpreadsheetRepo)

logger = logging.getLogger(__name__)

class OcgullFactory():
    @classmethod
    def create(cls, gcp_api_key, datasource, notify_via_email):
        """
        Create an Ocgull isinstance.

        :param gcp_api_key: The Google Cloud Platform API key.
        :param datasource: The datasource to read from.
        :param notify_via_email: Whether the created instance should send email
                notifications.
        """
        logger.info("Creating Ocgull with args: {}".format((datasource, notify_via_email)))

        repoconfig = RepoConfig(datasource)
        notifier = EmailNotifier() if notify_via_email else PrintNotifier()

        gull = Ocgull(SpreadsheetRepo(repoconfig, gcp_api_key),
                PreviousSpreadsheetRepo(repoconfig), notifier)

        return gull
