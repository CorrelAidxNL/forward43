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
        details = self.client.get_survey_details(survey_id)
        return details

    def get_respondent_ids(self, responses: dict):
        """Get id of respondent """
        """Note: multiple projects per respondent"""
        respondent_ids = []
        for dict_id in responses:
            for id in responses[dict_id]:
                respondent_ids.append(id)
        return respondent_ids

    def get_questions_dict(survey_details):
        questions = {}
        for page in survey_details['pages']:
            for question in page.get('questions', []):
                for row in question.get('answers', {}).get('rows', []):
                    questions[row['id']] = row['text']
        return questions


    def get_city_dict(responses_dict, respondent_ids, survey_id):
        """get respondent location: city"""
        city_dict = {}
        for respondent_id in respondent_ids:
            for page in responses_dict[survey_id][respondent_id]['pages']:
                if page['id'] == '146876559':
                    for question in page.get('questions', []):
                        for answer in question.get('answers', []):
                            if 'row_id' in answer:
                                if answer['row_id'] == '3771417351':
                                    city_dict[respondent_id] = answer['text']
        return city_dict

    def get_country_dict(responses_dict, respondent_ids, survey_id):
        """get respondent location: country"""
        country_dict = {}
        for respondent_id in respondent_ids:
            for page in responses_dict[survey_id][respondent_id]['pages']:
                if page['id'] == '146876559':
                    for question in page.get('questions', []):
                        for answer in question.get('answers', []):
                            if 'row_id' in answer:
                                if answer['row_id'] == '3771417354':
                                    country_dict[respondent_id] = answer['text']
        return country_dict

    def get_link_dict(responses_dict, respondent_ids, survey_id):
        """get respondent contact: link"""
        link_dict = {}
        for respondent_id in respondent_ids:
            for page in responses_dict[survey_id][respondent_id]['pages']:
                if page['id'] == '146876559':
                    for question in page.get('questions', []):
                        for answer in question.get('answers', []):
                            if 'row_id' in answer:
                                if answer['row_id'] == '3771417370':
                                    link_dict[respondent_id] = answer['text']
        return link_dict

    def get_titles_dict(responses_dict, respondent_ids, survey_id):
        """Get dict with a list of all project titles per respondent id"""
        titles_dict = {}
        for respondent_id in respondent_ids:
            for page in responses_dict[survey_id][respondent_id]['pages']:
                for question in page.get('questions', []):
                    if question['id'] in ['572537437', '572539926', '572540304', '572540360']:
                        for answer in question.get('answers', []):
                            key = respondent_id
                            titles_dict.setdefault(key, [])
                            titles_dict[key].append(answer['text'])
        return titles_dict

    def get_description_dict(responses_dict, respondent_ids, survey_id):
        """Get dict with a list of all project descriptions per respondent id"""
        description_dict = {}
        for respondent_id in respondent_ids:
            for page in responses_dict[survey_id][respondent_id]['pages']:
                for question in page.get('questions', []):
                    if question['id'] in ['572538644', '572539930', '572540308', '572540365']:
                        for answer in question.get('answers', []):
                            key = respondent_id
                            description_dict.setdefault(key, [])
                            description_dict[key].append(answer['text'])
        return description_dict

    def get_innovation_type_dict(responses_dict, respondent_ids, survey_id, choices_dict):
        """Get dict with list of innovation type per respondent id"""
        innovation_type_dict = {}
        for respondent_id in respondent_ids:
            for page in responses_dict[survey_id][respondent_id]['pages']:
                for question in page.get('questions', []):
                    if question['id'] in ['572538515', '572539929', '572540307', '572540364']:
                        for answer in question.get('answers', []):
                            if 'choice_id' in answer:
                                key = respondent_id
                                value = choices_dict[answer['choice_id']]
                                innovation_type_dict.setdefault(key, [])
                                innovation_type_dict[key].append(value)
        return innovation_type_dict







