from __future__ import print_function
import modelcatalog
from mint._utils import log
from modelcatalog.rest import ApiException

configuration = modelcatalog.Configuration()
USERNAME = "mint@isi.edu"
custom_query_name_config = ""

def get_model(_id):
    api_instance = modelcatalog.ModelApi()
    try:
        api_response = api_instance.models_id_get(id=_id)
        return api_response
    except ApiException as e:
        raise e

def list_model_configuration():
   api_instance = modelcatalog.ModelConfigurationApi()
   try:
       api_response = api_instance.modelconfigurations_get(username=USERNAME)
       return api_response
   except ApiException as e:
       raise e

def get_model_configuration(_id):
    api_instance = modelcatalog.ModelConfigurationApi()
    custom_query_name = 'custom_modelconfigurations'  # str | Name of the custom query (optional) (default to 'custom_modelconfigurations')
    try:
        api_response = api_instance.custom_modelconfigurations_id_get(_id, username=USERNAME, custom_query_name=custom_query_name)
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

def datasetspecifications_id_get(_id):
    try:
        # Get a DatasetSpecification
        api_instance = modelcatalog.DatasetSpecificationApi()
        api_response = api_instance.datasetspecifications_id_get(_id, username=USERNAME)
        return api_response
    except ApiException as e:
        print("Exception when calling DatasetSpecificationApi->datasetspecifications_id_get: %s\n" % e)