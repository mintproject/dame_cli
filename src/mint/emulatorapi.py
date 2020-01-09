from __future__ import print_function
import ingestion
from ingestion import Thread
from mint.downloader import get_json
from ingestion.rest import ApiException

def get_summary_from_dict(dict):
    thread_dict = dict['thread']
    thread = Thread(id=thread_dict["id"],
                    text=thread_dict["text"],
                    time_period=thread_dict["time_period"],
                    indicators=thread_dict["indicators"],
                    models=thread_dict["models"],
                    datasets=thread_dict["datasets"],
                    results=thread_dict["results"]
                    )
    return thread

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
        print(api_response)
        return api_response
    except ApiException as e:
        raise e

def obtain_results(thread_id, force=True):
    api_instance = ingestion.ResultApi()
    try:
        # Get a result
        print(thread_id)
        api_response = api_instance.results_thread_id_get(thread_id, force)
        return api_response
    except ApiException as e:
        raise ValueError("Not found")


def create_csv(scenario_id, problem_id, thread_id):
    api_instance = ingestion.SummaryApi()
    modelthread = ingestion.Modelthread(scenario_id=scenario_id, subgoal_id=problem_id, thread_id=thread_id)
    try:
        # Create a summary
        api_response = api_instance.summary_post(modelthread)
        return api_response
    except ApiException as e:
        print("Exception when calling DefaultApi->get_summary: %s\n" % e)