# -*- coding: utf-8 -*-
"""
Template tags to display buttons in pages

:creationdate: 09/01/2017 09:21
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: forms.models
"""
from __future__ import unicode_literals

import logging

import enum
from django import template
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger('buttons.templatetags.buttons_tags')

register = template.Library()


class IconPosition(enum.Enum):
    """
    Icon positions enumeration
    """

    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    NONE = 'NONE'


@register.inclusion_tag('buttons/button.html')
def button(**kwargs):
    """
    Displays a default button

    :param kwargs: Additional keyword args in:

    + `text`: Button text, default 'Button'
    + `icon`: Button icon, default ``None``
    + `icon_position`: Button icon position, , default ``None``, aka no icon displayed
    + `btn_css_class`: Button bootstrap class
    + `btn_id`: Button Id
    + `btn_url`: Button url. If set, a ``a`` tag us used instead of ``button``
    + `dismiss`: If `True`, the

    :returns: Render-able dict
    """
    text = kwargs.get('text', _('Button'))
    icon = kwargs.get('icon', None)
    icon_position = kwargs.get('icon_position', IconPosition.NONE)
    icon_css_class = kwargs.get('icon_css_class', None)
    btn_css_class = kwargs.get('btn_css_class', 'btn-default')
    btn_id = kwargs.get('id', None)
    btn_url = kwargs.get('url', None)
    data_dismiss = kwargs.get('data_dismiss', None)
    data_toggle = kwargs.get('data_toggle', None)
    data_target = kwargs.get('data_target', None)

    # Dict initialization
    output = {'text': text,
              'icon': icon,
              'icon_position': icon_position,
              'icon_css_class': icon_css_class,
              'btn_css_class': btn_css_class,
              'btn_type': 'button',
              'btn_id': btn_id,
              'btn_url': btn_url,
              # Data
              'data_dismiss': data_dismiss,
              'data_toggle': data_toggle,
              'data_target': data_target
              }

    return output


@register.inclusion_tag('buttons/button.html')
def download(text=_('Download'), icon='download', **kwargs):
    """
    Displays a ``download`` button

    :param text: Button text
    :param icon: Button icon
    :param kwargs: Additional keyword args in:

    + `icon_position`: Button icon position, , default ``None``, aka no icon displayed
    + `btn_css_class`: Button bootstrap class

    :returns: Render-able dict
    """
    return button(text=text, icon=icon, **kwargs)


@register.inclusion_tag('buttons/button.html')
def back(text=_('Back'), icon='chevron-left', icon_position=IconPosition.LEFT, btn_css_class='btn-primary', **kwargs):
    """
    Displays a ``back`` button

    :param text: Button text
    :param icon: Button icon
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.LEFT`
    :param btn_css_class: Button css class, default `btn-primary`
    :param kwargs: Additional keyword args in:

    + `btn_css_class`: Button bootstrap class

    :returns: Render-able dict
    """
    return button(text=text, icon=icon, icon_position=icon_position, url='javascript:history.back()', **kwargs)


@register.inclusion_tag('buttons/button.html')
def home(text=_('Home'), icon='home', icon_position=IconPosition.LEFT, btn_css_class='btn-primary', **kwargs):
    """
    Displays a ``back`` button

    :param text: Button text, default 'Home'
    :param icon: Button icon, default 'fa-home'
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_class: Button bootstrap class, default 'btn-primary'

    :returns: Render-able dict
    """
    return button(text=text, icon=icon, icon_position=icon_position, btn_css_class=btn_css_class, url='/', **kwargs)


@register.inclusion_tag('buttons/button.html')
def submit(text=_('Submit'), icon='check', icon_position=IconPosition.RIGHT, btn_css_class='btn-primary', **kwargs):
    """
    Displays a ``submit`` button


    :returns: Render-able dict
    """
    return button(text=text, btn_type='submit', icon=icon, icon_position=icon_position, btn_css_class=btn_css_class, **kwargs)

