"""Scaper for Masterpeace projects."""
import logging
from typing import Dict
import json

from surveymonkey import client
from forward43.scraper import ForwardScraper
from forward43.data.data_path import DATA_DIRECTORY

logger = logging.getLogger()


def get_client(token):
    """Get surveymonkey client."""
    surveymonkey_client = client.Client(access_token=token)

    return surveymonkey_client


class MasterpeaceScraper(ForwardScraper):
    """Scrapes Masterpeace clubs' reports of projects."""
    def __init__(self, token: str, use_local: bool = False):
        ForwardScraper.__init__(self, "masterpeace")
        self.use_local = use_local
        self.client = get_client(token)

    def scrape(self):
        """Scrape surveys."""
        pass

    def get_survey_responses(self, search_string: str) -> Dict[str, Dict]:
        """Get surveys for Masterpeace projects that have the search string in their title.

        Returns:
            Dict[survey_id : Dict of responses]
        """
        if self.use_local:
            with open(DATA_DIRECTORY + "/surveys.json") as fh:
                surveys = json.load(fh)
            return surveys
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
                    respondent_id = response_data.get("id", "")
                    returnable_responses[survey_id][respondent_id] = response_data

        return returnable_responses

    def get_survey_questions(self, survey_id: str) -> Dict[str, str]:
        """Get the questions associated with the row number in a survey."""
        pass
        self.client.get_survey_page_questions(survey_id)

    def get_survey_choices(self, details: dict) -> Dict[str, str]:
        """Get closed answer choices to questions."""
        choices = {}
        for page in details["pages"]:
            for question in page.get("questions", []):
                if question["family"] == "multiple_choice" or question["family"] == "single_choice":
                    for choice in question.get("answers", {}).get("choices", []):
                        choices[choice["id"]] = choice["text"]
        return choices

    def get_survey_details(self, survey_id: str) -> Dict[str, str]:
        """Get survey details."""
        if self.use_local:
            with open(DATA_DIRECTORY + "/survey_details.json") as fh:
                details = json.load(fh)
        else:
            details = self.client.get_survey_details(survey_id)
        return details
