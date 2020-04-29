from __future__ import print_function
import modelcatalog
from modelcatalog import ApiClient
from modelcatalog.rest import ApiException

from dame.configuration import get_credentials

USERNAME = "mint@isi.edu"


def api_configuration(profile):
    credentials = get_credentials(profile)
    if credentials is None:
        return modelcatalog.configuration(), USERNAME
    configuration = modelcatalog.Configuration()
    configuration.host = credentials["server"]
    return ApiClient(configuration=configuration), credentials["username"]


def list_model_configuration(label=None, profile="default"):
    api, username = api_configuration(profile)
    api_instance = modelcatalog.ModelConfigurationApi(api)
    try:
        api_response = api_instance.modelconfigurations_get(username=username)
        return api_response
    except ApiException as e:
        raise e


def get_model_configuration(_id, profile="default"):
    api, username = api_configuration(profile)
    api_instance = modelcatalog.ModelConfigurationApi(api)
    try:
        api_response = api_instance.custom_modelconfigurations_id_get(_id, username=username)
        return api_response
    except ApiException as e:
        raise e


def get_setup(_id, profile="default"):
    api, username = api_configuration(profile)
    api_instance = modelcatalog.ModelConfigurationSetupApi(api)
    try:
        # Get a ModelConfiguration
        api_response = api_instance.custom_modelconfigurationsetups_id_get(_id, username=username)
        return api_response
    except ApiException as e:
        raise e


def list_setup(label=None, profile="default"):
    api, username = api_configuration(profile)
    api_instance = modelcatalog.ModelConfigurationSetupApi(api)
    try:
        # Get a ModelConfigurationSetup
        api_response = api_instance.modelconfigurationsetups_get(username=username)
        return api_response
    except ApiException as e:
        raise e
