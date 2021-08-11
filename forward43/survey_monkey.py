from surveymonkey.client import Client
import requests
import json



ACCESS_TOKEN		= access_token
CLIENT_SECRET       = "56520454083989005311023350857684991904"

SURVEY_ID           = "297005313"


# If you have access_token, run
client	        	=		Client(
                                client_secret		= CLIENT_SECRET,
                                access_token		= ACCESS_TOKEN
)


s = requests.Session()
s.headers.update({
    "Authorization": "Bearer %s" % ACCESS_TOKEN,
    "Content-Type": "application/json"
})


# get survey details
survey_details_url  = "https://api.surveymonkey.com/v3/surveys/%s/details" % (SURVEY_ID)
survey_details      = s.get(survey_details_url)


# get (100) survey responses
payload = {
 "type": "weblink"
}


survey_responses_url = "https://api.surveymonkey.com/v3/surveys/%s/collectors" % (SURVEY_ID)
# s.post(survey_responses_url, json = payload)
