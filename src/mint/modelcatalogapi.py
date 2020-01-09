from __future__ import print_function
import modelcatalog
from modelcatalog.rest import ApiException

configuration = modelcatalog.Configuration()
USERNAME = "mint@isi.edu"


def get_model(_id):
    api_instance = modelcatalog.ModelApi()
    try:
        api_response = api_instance.models_id_get(id=_id)
        return api_response
    except ApiException as e:
        raise e


def get_setup(_id):
    # create an instance of the API class
    api_instance = modelcatalog.ConfigurationSetupApi()
    custom_query_name = 'custom_configurationsetups'  # str | Name of the custom query (optional) (default to 'custom_configurationsetups')
    try:
        # Get a ModelConfigurationSetup
        api_response = api_instance.custom_configurationsetups_id_get(_id, username=USERNAME, custom_query_name=custom_query_name)
        return api_response
    except ApiException as e:
        raise e


def list_setup(label=None):
    # create an instance of the API class
    api_instance = modelcatalog.ConfigurationSetupApi()
    try:
        # Get a ModelConfigurationSetup
        api_response = api_instance.configurationsetups_get(username=USERNAME)
        return api_response
    except ApiException as e:
        raise e
