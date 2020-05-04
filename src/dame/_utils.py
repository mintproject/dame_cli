# -*- coding: utf-8 -*-
import logging.config
import requests

log = logging.getLogger()


def init_logger():
    LOGLEVEL = logging.DEBUG
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                # exact format is not important, this is the minimum information
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            },
        },
        'handlers': {
            # console logs to stderr
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'loggers': {
            # default for all undefined Python modules
            '': {
                'level': 'DEBUG',
                'handlers': ['console'],
            },
            # Our application code
            'wcm': {
                'level': LOGLEVEL,
                'handlers': ['console'],
                # Avoid double logging because of root logger
                'propagate': False,
            },
            # Prevent noisy modules from logging to Sentry
            'noisy_module': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    })
    logger = logging.getLogger(__package__)


def get_latest_version():
    return requests.get("https://pypi.org/pypi/dame-cli/json").json()["info"]["version"]
