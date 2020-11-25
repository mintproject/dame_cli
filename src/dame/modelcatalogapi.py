from __future__ import print_function

import click
import modelcatalog
from modelcatalog import ApiClient
from modelcatalog.rest import ApiException

from dame.configuration import get_credentials, DEFAULT_PROFILE

USERNAME = "mint@isi.edu"


def api_configuration(profile):
    credentials = get_credentials(profile)
    if credentials is None:
        return ApiClient(), USERNAME
    configuration = modelcatalog.Configuration()
    package_version = configuration.host.split('/')[-1].replace("v", '')
    configuration_version = credentials["server"].split('/')[-1].replace("v", '')
    if package_version > configuration_version:
        click.secho(
            f"""WARNING: Your credentials are using Model Catalog version {configuration_version},
            but the version {package_version} is available.
            You should consider upgrading via the 'dame configure -p {profile}'""",
            fg="yellow",
        )
        click.secho("DAME is going to use the newest version", fg="yellow")
    else:
        configuration.host = credentials["server"]
    return ApiClient(configuration=configuration), credentials["username"]


def list_model_configuration(label=None, profile=DEFAULT_PROFILE):
    api, username = api_configuration(profile)
    api_instance = modelcatalog.ModelConfigurationApi(api)
    try:
        api_response = api_instance.modelconfigurations_get(username=username)
        return api_response
    except ApiException as e:
        raise e


def get_data_transformation(profile=DEFAULT_PROFILE):
    api, username = api_configuration(profile)
    api_instance = modelcatalog.DataTransformationApi(api)
    try:
        api_response = api_instance.datatransformations_get(username=username)
        return api_response
    except ApiException as e:
        raise e


def get_model_configuration(_id, profile=DEFAULT_PROFILE):
    api, username = api_configuration(profile)
    api_instance = modelcatalog.ModelConfigurationApi(api)
    try:
        api_response = api_instance.custom_modelconfigurations_id_get(_id, username=username)
        return api_response
    except ApiException as e:
        raise e


def get_setup(_id, profile=DEFAULT_PROFILE):
    api, username = api_configuration(profile)
    api_instance = modelcatalog.ModelConfigurationSetupApi(api)
    try:
        # Get a ModelConfiguration
        api_response = api_instance.custom_modelconfigurationsetups_id_get(_id, username=username)
        return api_response
    except ApiException as e:
        raise e


def list_setup(label=None, profile=DEFAULT_PROFILE):
    api, username = api_configuration(profile)
    api_instance = modelcatalog.ModelConfigurationSetupApi(api)
    try:
        # Get a ModelConfigurationSetup
        api_response = api_instance.modelconfigurationsetups_get(username=username)
        return api_response
    except ApiException as e:
        raise e


def get_transformation_dataset(data_specification_id, profile=DEFAULT_PROFILE):
    # Create an instance of the API class

    items = []
    return items;
    #FIXME: I do no find this query on the server.

    api, username = api_configuration(profile)
    api_instance = modelcatalog.DataTransformationApi(api)
    custom_query_name = 'custom_datatransformations'  # str | Name of the custom query (optional) (default to 'custom_datatransformations')

    try:
        # Gets a list of data transformations related a dataset
        api_response = api_instance.\
                                    custom_dataspecifications_id_datatransformations_get(
                                        data_specification_id,
                                        custom_query_name=custom_query_name,
                                        username=username)

        for i in api_response:
            if i.id:
                items.append(i)


        return items
    except ApiException as e:
        raise e

