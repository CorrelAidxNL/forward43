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

        for survey_id in scrapable_surveys.keys():
            responses_dict[survey_id] = {}
            responses = self.client.get_all_pages_response(survey_id)
            for response in responses:
                if not response.get("data", []):
                    raise ValueError(
                        f"Responses not found for survey_id {survey_id}, data returned: {responses}"
                    )
                for response_data in response.get("data"):
                    respondent_id = response_data.get("id", "")
                    responses_dict[survey_id][respondent_id] = response_data

        return responses_dict

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

    def get_questions_dict(self, survey_details):
        questions = {}
        for page in survey_details['pages']:
            for question in page.get('questions', []):
                for row in question.get('answers', {}).get('rows', []):
                    questions[row['id']] = row['text']
        return questions

    def get_titles_list(self, responses, respondent_id, survey_id, project_data_dict):
        """Get dict with a list of all project titles per respondent id"""
        titles_list = []
        for page in responses[survey_id][respondent_id]['pages']:
            for question in page.get('questions', []):
                if question['id'] in project_data_dict['Project Title']:
                    for answer in question.get('answers', []):
                        key = respondent_id
                        titles_list.setdefault(key, [])
                        titles_list[key].append(answer['text'])
        return titles_list

    def get_innovation_type(self, responses, respondent_id, survey_id, project_data_dict, choices_dict):
        """Get list of related MasterPeace activities and SDGs"""
        innovation_type_list = []
        for page in responses[survey_id][respondent_id]['pages']:
            for question in page.get('questions', []):
                if question['id'] in [project_data_dict['Related MasterPeace core activity: (possible to tick multiple)'] or project_data_dict['Related SDGs: (possible to tick multiple)']]:
                    for answer in question.get('answers', []):
                        if 'choice_id' in answer:
                            value = choices_dict[answer['choice_id']]
                            innovation_type_list.append(value)
        return innovation_type_list

    def get_club_data_ids(self, survey_details: dict) -> Dict[str, str]:
        """Get ids of the answers to questions on club data."""
        club_data = {}
        for page in survey_details["pages"]:
            for question in page.get("questions", []):
                if question["family"] == "demographic" or question["family"] == "open_ended":
                    for row in question.get("answers", {}).get("rows", []):
                        if 'type' in row:
                            club_data[row["id"]] = row["type"]
        return club_data

    def get_project_data_ids(self, survey_details: dict):
        """Get ids of the answers to questions on projects."""
        project_data_ids = {}
        for page in survey_details["pages"]:
            for question in page.get("questions", []):
                if 'headings' in question:
                    if len(question["headings"]) > 0:
                        project_data_ids[question['id']] = question['headings'][0].get('heading', "")
        return project_data_ids

    def split_project_dict(self, project_data_ids: dict):
        """split project_data_ids dict with duplicate values into 1 dict per project (max 4)"""
        unique_values = list(set(project_data_ids.values()))
        split_project_dict = {}
        for x in unique_values:
            ids_per_value = [key for key, value in project_data_ids.items() if value == x]
            ids_per_value.sort()
            if len(ids_per_value) > 1:
                split_project_dict[x] = ids_per_value
        return split_project_dict

    def get_respondent_data(self, responses, survey_id, respondent_id, club_data_dict, entity) -> str:
        """get data entities per respondent"""
        for page in responses[survey_id][respondent_id]['pages']:
            if page['id'] == '146876559':
                for question in page.get('questions', []):
                    for answer in question.get('answers', []):
                        if 'row_id' in answer:
                            if answer['row_id'] == club_data_dict[entity]:
                                return answer['text']


    def get_project_data(self, responses, survey_id, respondent_id, split_project_data_dict, project_number, entity) -> str:
        """get data entities per project"""
        for page in responses[survey_id][respondent_id]['pages']:
            for question in page.get('questions', []):
                if question['id'] in split_project_data_dict[entity][project_number]:
                    for answer in question.get('answers', []):
                        return answer['text']

    def process_response(self, responses, survey_details, survey_id, respondent_id):
        """process survey data per respondent id"""
        club_data_dict = self.get_club_data_ids(survey_details)
        project_data_dict = self.get_project_data_ids(survey_details)
        split_project_data_dict = self.split_project_dict(project_data_dict)
        choices_dict = self.get_survey_choices(survey_details)

        titles_list = self.get_titles_list(responses, respondent_id, survey_id, project_data_dict)
        num_projects = len(titles_list)
        project_list = []

        # get club data
        country = self.get_respondent_data(responses, survey_id, respondent_id, club_data_dict, entity = 'country')
        city    = self.get_respondent_data(responses, survey_id, respondent_id, club_data_dict, entity = 'city')
        contact = self.get_respondent_data(responses, survey_id, respondent_id, club_data_dict, entity = 'email')

        for i in range(num_projects):
            project_list.append({
                'id'              : 'respondent_id'+ str(i),
                'title'           : self.get_project_data(responses, survey_id, respondent_id, split_project_data_dict, project_number = i, entity = 'Project Title'),
                'description'     : self.get_project_data(responses, survey_id, respondent_id, split_project_data_dict, project_number = i, entity = 'Describe your project (at least 300 words)<br><br><em>- Context (What is the dilemma that the project is trying to tackle? Why is it important for this neighbourhood/group of people/the country?</em><br><em>- Activities (What did you do?)</em><br><em>- Results (What did you achieve? What did you create, produce, accomplish? Try to include numbers, if possible).</em><br><em>- Impact (What changed in the community? What did you learn yourself or as a team? Did you meet your own expectations)?</em>'),
                'status'          : 'n.a.',
                'innovation_type' : self.get_innovation_type(responses, respondent_id, survey_id, project_data_dict, choices_dict),
                'country'         : country,
                'city'            : city,
                'contact'         : contact,
                'link'            : self.get_project_data(responses, survey_id, respondent_id, split_project_data_dict, project_number = i, entity = 'Which media channels did you use? Can you share links to your social media posts or any\xa0external publications?')
            })

        return project_list

    def scrape(self, search_string, survey_id):
        ''' Main Scraper function '''
        responses       = self.get_survey_responses(search_string)
        survey_details  = self.get_survey_details(survey_id)
        respondent_ids  = self.get_respondent_ids(responses)

        for respondent_id in respondent_ids:
            self.logger.info(f'Processing survey response from respondent {respondent_id}')

            try:
                projects        = self.process_response(responses, survey_details, survey_id, respondent_id)

            except Exception as e:
                self.logger.exception('Failed to get projects from current page')

            self.write_to_file(projects, str(search_string + respondent_id))

if __name__ == '__main__':

    scraper = MasterpeaceScraper(search_string = "MEAL", survey_id = '297005313')
    scraper.scrape()







