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
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger('buttons.buttons_tags')

register = template.Library()


class IconPosition(enum.Enum):
    """
    Icon positions enumeration
    """

    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    NONE = 'NONE'


@register.inclusion_tag('buttons/button.html')
def btn_button(**kwargs):
    """
    Displays a default button

    :param kwargs: Additional keyword args in:

    + `text`: Button text, default 'Button'
    + `url`: Target URL, if needed
    + `icon`: Button icon, default ``None``
    + `icon_position`: Button icon position, , default ``None``, aka no icon displayed
    + `btn_css_class`: Button bootstrap class
    + `btn_id`: Button Id
    + `btn_url`: Button url. If set, a ``a`` tag us used instead of ``button``
    + `dismiss`: If `True`, the

    :returns: Render-able dict
    """
    logger.debug('btn_button() kwargs = %s', kwargs)

    text = kwargs.pop('text', _('Button'))
    url = kwargs.pop('url', None)
    href_target = kwargs.pop('href_target', None)

    icon = kwargs.pop('icon', settings.BUTTONS_ICON)
    icon_position = kwargs.pop('icon_position', settings.BUTTONS_ICON_POSITION)
    icon_css_extra = kwargs.pop('icon_css_extra', settings.BUTTONS_ICON_CSS_EXTRA)

    btn_css_color = kwargs.pop('btn_css_color', settings.BUTTONS_BTN_CSS_COLOR)
    btn_css_extra = kwargs.pop('btn_css_extra', settings.BUTTONS_BTN_CSS_EXTRA)
    btn_id = kwargs.pop('id', None)

    data_dismiss = kwargs.pop('data_dismiss', None)
    data_toggle = kwargs.pop('data_toggle', None)
    data_target = kwargs.pop('data_target', None)

    # Dict initialization
    output = {'text': text,
              'url': url,
              'href_target': href_target,
              # ison informations
              'icon': icon,
              'icon_position': icon_position,
              'icon_css_extra': icon_css_extra,
              # btn informations
              'btn_css_color': btn_css_color,
              'btn_css_extra': btn_css_extra,
              'btn_type': 'button',
              'btn_id': btn_id,
              # `data-*` fields
              'data_dismiss': data_dismiss,
              'data_toggle': data_toggle,
              'data_target': data_target
              }

    return output


@register.inclusion_tag('buttons/button.html')
def btn_download(url, text=_('Download'), icon='download', icon_position=IconPosition.RIGHT, **kwargs):
    """
    Displays a ``download`` button

    :param url: **Mandatory** target url
    :param text: Button text
    :param icon: Button icon
    :param kwargs: Additional keyword args in:

    + `btn_css_class`: Button bootstrap class

    :returns: Render-able dict
    """
    return btn_button(url=url, text=text, icon=icon, icon_position=icon_position, **kwargs)


@register.inclusion_tag('buttons/button.html')
def btn_back(text=_('Back'), icon='chevron-left', icon_position=IconPosition.LEFT, btn_css_color='btn-primary', **kwargs):
    """
    Displays a ``btn_back`` button

    :param text: Button text
    :param icon: Button icon
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.LEFT`
    :param btn_css_color: Button css class, default `btn-primary`
    :param kwargs: Additional keyword args in:

    + `btn_css_class`: Button bootstrap class

    :returns: Render-able dict
    """
    return btn_button(text=text, icon=icon, icon_position=icon_position, btn_css_color='btn-primary',
                      url='javascript:history.btn_back()', **kwargs)


@register.inclusion_tag('buttons/button.html')
def btn_link(url, text=_('Link'), icon='btn_link', icon_position=IconPosition.LEFT,
             btn_css_color='btn-default', **kwargs):
    """
    Displays a simple ``link`` btn_button

    :param url: **Mandatory** target url
    :param text: link text, default 'link'
    :param icon: Icon label, default 'link'
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Button bootstrap class, default 'btn-default'

    :param kwargs:

    :returns: Render-able dict
    """
    return btn_button(url=url, text=text, icon=icon, icon_position=icon_position,
                      btn_css_color=btn_css_color, **kwargs)


@register.inclusion_tag('buttons/button.html')
def btn_home(url='/', text=_('Home'), icon='home', icon_position=IconPosition.LEFT, btn_css_color='btn-primary',
             **kwargs):
    """
    Displays a ``btn_back`` btn_button

    :param url: Target URL, default '/'
    :param text: Button text, default 'Home'
    :param icon: Button icon, default 'fa-home'
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Button bootstrap class, default 'btn-primary'
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    return btn_button(url=url, text=text, icon=icon, icon_position=icon_position, btn_css_color=btn_css_color,
                      **kwargs)


@register.inclusion_tag('buttons/button.html')
def btn_submit(text=_('Submit'), icon='check', btn_css_color='btn-primary', **kwargs):
    """
    Displays a ``submit`` button

    :param text: Button text, default 'Submit'
    :param icon: Button icon, default 'check'
    :param btn_css_color: Base button color
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    return btn_button(text=text, btn_type='submit', icon=icon, btn_css_color=btn_css_color, **kwargs)


@register.inclusion_tag('buttons/button.html')
def btn_list(url, text=_('List'), icon='list', btn_css_color='btn-primary', **kwargs):
    """
    Displays a ``list`` button

    :param url: **Mandatory** target url
    :param text: Button text, default 'Submit'
    :param icon: Button icon, default 'check'
    :param btn_css_color: Base button color
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    return btn_button(url=url, text=text, icon=icon, btn_css_color=btn_css_color, **kwargs)


@register.inclusion_tag('buttons/button.html')
def btn_search(url, text=_('Search'), **kwargs):
    return btn_button(url=url, text=text, **kwargs)


@register.inclusion_tag('buttons/button.html')
def btn_close(btn_css_color='btn-warning'):
    return btn_button(btn_css_color=btn_css_color)


@register.inclusion_tag('buttons/button.html')
def btn_login(url, text=_('Login'), icon='login', **kwargs):
    return btn_button(url=url, text=text, icon=icon, **kwargs)
