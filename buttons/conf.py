# -*- coding: utf-8 -*-
"""
Configuration values for the :mod:`buttons:buttons` application

:creationdate: 09/01/17 12:48
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: buttons.conf

"""

import logging

from appconf import AppConf

__author__ = 'fguerin'
logger = logging.getLogger('buttons.conf')


class ButtonsAppConf(AppConf):
    """
    App con for :mod:`buttons:buttons` application
    """
    ICON_POSITION = 'RIGHT'
    ICON = 'exclamation'
    ICON_CSS_EXTRA = ''

    FONTAWESOME_VERSION = 5

    BTN_CSS_COLOR = 'btn-default'
    BTN_CSS_EXTRA = 'btn-sm'

    class Meta:
        prefix = 'buttons'
