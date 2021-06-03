"""Scaper for Masterpeace projects."""
from typing import Dict, List

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

    def get_survey_responses(self, search_string: str) -> List[Dict]:
        """Get the correct surveys for Masterpeace projects."""
        surveys = self.client.get_survey_lists()
        if 'data' not in surveys:
            raise ValueError(
                f"Surveys not found for search string {search_string}, data returned: {surveys}"
            )

        scrapable_surveys = {}
        for survey in surveys["data"]:
            if search_string in survey["title"]:
                scrapable_surveys[survey["id"]] = survey

        if len(scrapable_surveys) == 0:
            raise ValueError(
                f"Surveys not found for search string {search_string}, data returned: {surveys}"
            )

        returnable_responses = {}
        for survey_id in scrapable_surveys.keys():
            returnable_responses[survey_id] = {}
            responses = self.client.get_all_pages_response(survey_id)
            for response in responses:
                if not response.get("data", []):
                    raise ValueError(
                        f"Responses not found for survey_id {survey_id}, data returned: {responses}"
                    )
                for response_data in response.get("data"):
                    respondant_id = response_data.get("id", "")
                    returnable_responses[survey_id][respondant_id] = response_data

        return returnable_responses

        return returnable_surveys
