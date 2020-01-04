from __future__ import print_function
import ingestion
from ingestion import Configuration
from ingestion.rest import ApiException


def get_thread(thread_id):
    api_instance = ingestion.ThreadApi()
    try:
        # Get a ModelConfigurationSetup
        api_response = api_instance.modelthreads_thread_id_get(thread_id)
        return api_response
    except ApiException as e:
        raise e


def list_threads(limit=200, page=1, model=""):
    configuration = Configuration()
    configuration.host = "http://localhost:8080/v1.2.0"
    # create an instance of the API class
    api_instance = ingestion.ThreadApi(ingestion.ApiClient(configuration))
    try:
        # Get a ModelConfigurationSetup
        api_response = api_instance.getthreads(limit=limit, page=page, model=model)
        return api_response
    except ApiException as e:
        raise e
