# -*- coding: utf-8 -*-
"""
Django application config

:creationdate: 09/02/17 15:47
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: buttons.apps

"""

import logging
from django.apps import AppConfig

__author__ = 'fguerin'
logger = logging.getLogger('buttons.apps')


class ButtonsAppConfig(AppConfig):
    name = 'buttons'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from buttons.conf import ButtonsAppConf
