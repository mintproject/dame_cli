from __future__ import print_function
import ingestion
from ingestion import Configuration
from ingestion.rest import ApiException

configuration = Configuration()
configuration.host = "http://localhost:8080/v1.2.0"

def get_summary(thread_id):
    api_instance = ingestion.SummaryApi()
    try:
        api_response = api_instance.summary_thread_id_get(thread_id)
        return api_response
    except ApiException as e:
        raise e


def list_summaries(limit=200, page=1, model=""):
    # create an instance of the API class
    api_instance = ingestion.SummaryApi()
    try:
        api_response = api_instance.summary_get(limit=limit, page=page, model=model)
        return api_response
    except ApiException as e:
        raise e
