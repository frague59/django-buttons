"""
Configuration values for the :mod:`buttons:buttons` application

:creationdate: 09/01/17 12:48
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: buttons.conf

"""

import logging

from appconf import AppConf

__author__ = "fguerin"
logger = logging.getLogger("buttons.conf")


class ButtonsAppConf(AppConf):
    """
    App con for :mod:`buttons:buttons` application
    """

    ICON_POSITION: str = "RIGHT"
    ICON: str = "exclamation"
    ICON_CSS_EXTRA: str = ""

    FONTAWESOME_VERSION: int = 5

    BTN_CSS_COLOR: str = "btn-default"
    BTN_CSS_EXTRA: str = "btn-sm"

    DEFAULT_TEMPLATE_PATH: str = "buttons/{package}/button.html"

    class Meta:
        prefix = "buttons"
