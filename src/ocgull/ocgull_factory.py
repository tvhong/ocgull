import logging

from ocgull.notifier import EmailNotifier, PrintNotifier
from ocgull.ocgull import Ocgull
from ocgull.spreadsheet.repo import (
    PreviousSpreadsheetRepo, RepoConfig, SpreadsheetRepo)

logger = logging.getLogger(__name__)

class OcgullFactory():
    @classmethod
    def create(cls, gcp_api_key, datasource, email_addresses):
        """
        Create an Ocgull isinstance.

        :param gcp_api_key: The Google Cloud Platform API key.
        :param datasource: The datasource to read from.
        :param email_addresses: A list of email addresses to get nofication. If
                there's no addresses, result will be printed to stdout.
        """
        logger.info("Creating Ocgull with args: {}".format((datasource, email_addresses)))

        repoconfig = RepoConfig(datasource)
        notifier = EmailNotifier(email_addresses) if email_addresses else PrintNotifier()

        gull = Ocgull(SpreadsheetRepo(repoconfig, gcp_api_key),
                PreviousSpreadsheetRepo(repoconfig), notifier)

        return gull
