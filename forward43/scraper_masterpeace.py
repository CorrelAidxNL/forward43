"""Scaper for Masterpeace projects."""

from surveymonkey import client
from forward43.scraper import ForwardScraper


def get_client(token):
    """Get surveymonkey client."""
    surveymonkey_client = client.Client(access_token=token)

    return surveymonkey_client


class MasterpeaceScraper(ForwardScraper):
    """Scrapes Masterpeace clubs' reports of projects."""
    def __init__(self, token: str):
        ForwardScraper.__init__(self, 'masterpeace')

        self.client = get_client(token)

    def scrape(self):
        """Scrape surveys."""
        pass
        # surveys = self.client.get_survey_lists()
        #
        # return surveys
