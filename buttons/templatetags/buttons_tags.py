# -*- coding: utf-8 -*-
"""
Template tags to display buttons in pages

:creationdate: 09/01/2017 09:21
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: forms.models
"""

import logging

import enum
from django import template
from django.conf import settings
from django.forms.utils import flatatt
from django.utils.translation import ugettext as _

logger = logging.getLogger('buttons.templatetags.buttons_tags')

register = template.Library()


class IconPosition(enum.Enum):
    """
    Icon positions enumeration
    """

    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    ONLY = 'ONLY'
    NONE = 'NONE'


def _get_param(key, context, kwargs, default=None):
    return context.get(key) or kwargs.pop(key, None) or default


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_button(context, **kwargs):
    """
    Displays a default button

    :param context: Context data
    :param kwargs: Additional keyword args in:

    + `text`: Button text, default 'Button'
    + `url`: Target URL, if needed
    + `icon`: Button icon, default ``None``, from `FontAwesome <http://fontawesome.io/icons/>`_
    + `icon_position`: Button icon position, , default ``None``, aka no icon displayed
    + `btn_css_class`: Button bootstrap class
    + `btn_id`: Button Id
    + `btn_url`: Button url. If set, a ``a`` tag us used instead of ``button``
    + `data_dismiss`: Set ``data-dismiss`` HTML attribute
    + `data_toggle`: Set ``data-toggle`` HTML attribute
    + `data_placement`: Set ``data-placement`` HTML attribute
    + `data_target`: Set ``data-target`` HTML attribute

    :returns: Render-able dict
    """
    # logger.debug('btn_button() context = %s', unidecode(context))
    # logger.debug('btn_button() kwargs = %s', kwargs)

    text = _get_param('text', context, kwargs)
    url = _get_param('url', context, kwargs)
    _type = _get_param('btn_type', context, kwargs, 'button')
    btn_id = _get_param('id', context, kwargs) or _get_param('btn_id', context, kwargs)

    tooltip = _get_param('tooltip', context, kwargs)

    icon = _get_param('icon', context, kwargs, settings.BUTTONS_ICON)

    icon_position = _get_param('icon_position', context, kwargs, settings.BUTTONS_ICON_POSITION)
    if isinstance(icon_position, IconPosition):
        icon_position = icon_position.value
    else:
        icon_position = icon_position.upper()

    icon_css_extra = _get_param('icon_position', context, kwargs, settings.BUTTONS_ICON_CSS_EXTRA)

    btn_css_color = _get_param('btn_css_color', context, kwargs, settings.BUTTONS_BTN_CSS_COLOR)
    btn_css_extra = _get_param('btn_css_extra', context, kwargs, settings.BUTTONS_BTN_CSS_EXTRA)

    data_dismiss = _get_param('data_dismiss', context, kwargs)
    data_toggle = _get_param('data_toggle', context, kwargs)
    data_target = _get_param('data_target', context, kwargs)
    data_placement = _get_param('data_placement', context, kwargs)

    href_target = _get_param('href_target', context, kwargs)

    # Dict initialization
    output = {'text': text,
              'url': url,
              'href_target': href_target,

              # tooltip
              'tooltip': tooltip,

              # icon informations
              'icon': icon,
              'icon_position': icon_position,
              'icon_css_extra': icon_css_extra,

              # btn informations
              'btn_css_color': btn_css_color,
              'btn_css_extra': btn_css_extra,
              'btn_type': _type,
              'btn_id': btn_id,

              # `data-*` fields
              'data_dismiss': data_dismiss,
              'data_toggle': data_toggle,
              'data_target': data_target,
              'data_placement': data_placement,
              'debug': settings.DEBUG, }
    if kwargs:
        output.update({'flatatt': flatatt(kwargs)})

    # logger.debug('btn_button() output = %s', output)

    return output


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_download(context, url, text=_('Download'), icon='download', icon_position=IconPosition.RIGHT, **kwargs):
    """
    Displays a ``download`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Download'
    :param icon: Button icon, default `download <http://fontawesome.io/icon/download/>`
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param kwargs: Additional keyword args in:

    + `btn_css_class`: Button bootstrap class

    :returns: Render-able dict
    """
    return btn_button(context, url=url, text=text, icon=icon, icon_position=icon_position, **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_back(context, text=_('Back'), icon='chevron-left', icon_position=IconPosition.LEFT, btn_css_color='btn-primary',
             **kwargs):
    """
    Displays a ``btn_back`` button

    :param context: Context data
    :param text: Button text, default 'Back'
    :param icon: Button icon, default `chevron-left <http://fontawesome.io/icon/chevron-left/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.LEFT`
    :param btn_css_color: Button css class, default ``btn-primary``
    :param kwargs: Additional keyword args in:

    + `btn_css_class`: Button bootstrap class

    :returns: Render-able dict
    """
    return btn_button(context, text=text, icon=icon, icon_position=icon_position, btn_css_color=btn_css_color,
                      url='javascript:history.back()', **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_link(context, url, text=_('Link'), icon='link', icon_position=IconPosition.RIGHT,
             btn_css_color='btn-default', **kwargs):
    """
    Displays a simple ``link`` btn_button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: link text, default 'link'
    :param icon: Icon label, default `link <http://fontawesome.io/icon/link/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.LEFT`
    :param btn_css_color: Button bootstrap class, default 'btn-default'

    :param kwargs:

    :returns: Render-able dict
    """
    return btn_button(context, url=url, text=text, icon=icon, icon_position=icon_position,
                      btn_css_color=btn_css_color, **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_home(context, url='/', text=_('Home'), icon='home', icon_position=IconPosition.LEFT,
             btn_css_color='btn-primary', **kwargs):
    """
    Displays a ``btn_back`` btn_button

    :param context: Context data
    :param url: Target URL, default '/'
    :param text: Button text, default 'Home'
    :param icon: Button icon, default `home <http://fontawesome.io/icon/home/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.LEFT`
    :param btn_css_color: Button bootstrap class, default 'btn-primary'
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    return btn_button(context, url=url, text=text, icon=icon, icon_position=icon_position, btn_css_color=btn_css_color,
                      **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_submit(context, text=_('Submit'), icon='check', icon_position=IconPosition.RIGHT, btn_css_color='btn-primary',
               **kwargs):
    """
    Displays a ``submit`` button

    :param context: Context data
    :param text: Button text, default 'Submit'
    :param icon: Button icon, default `check <http://fontawesome.io/icon/check/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    return btn_button(context, text=text, btn_type='submit', icon=icon, btn_css_color=btn_css_color,
                      icon_position=icon_position, **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_list(context, url, text=_('List'), icon='list', icon_position=IconPosition.RIGHT, btn_css_color='btn-primary',
             **kwargs):
    """
    Displays a ``list`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Submit'
    :param icon: Button icon, default `list <http://fontawesome.io/icon/list/>`
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    return btn_button(context, url=url, text=text, icon=icon, icon_position=icon_position, btn_css_color=btn_css_color,
                      **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_detail(context, url, text=_('Detail'), icon='info', icon_position=IconPosition.RIGHT,
               btn_css_color='btn-primary', **kwargs):
    """
    Displays a `Detail` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Submit'
    :param icon: Button icon, default `info <http://fontawesome.io/icon/info/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.LEFT`
    :param btn_css_color: Base button color
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    return btn_button(context, url=url, text=text, icon=icon, icon_position=icon_position, btn_css_color=btn_css_color,
                      **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_create(context, url, text=_('Create'), icon='plus', icon_position=IconPosition.RIGHT,
               btn_css_color='btn-primary', **kwargs):
    """
    Displays a `Create` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Create'
    :param icon: Button icon, default `plus <http://fontawesome.io/icon/plus/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-primary`
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    logger.debug('btn_create() url = *%s*', url)
    return btn_button(context, url=url, text=text, icon=icon, icon_position=icon_position,
                      btn_css_color=btn_css_color, **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_search(context, text=_('Search'), icon='search', icon_position=IconPosition.RIGHT,
               btn_css_color='btn-default', **kwargs):
    """
    Renders a `Search` button

    :param context: Context data
    :param text: Button text, default 'Search'
    :param icon: Button icon, default `search <http://fontawesome.io/icon/search/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-default`
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    return btn_button(context, type='submit', text=text, icon=icon, icon_position=icon_position,
                      btn_css_color=btn_css_color, **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_close(context, text, icon='times', icon_position=IconPosition.RIGHT, btn_css_color='btn-warning',
              data_dismiss=True, **kwargs):
    """
    Renders a `Close` button

    :param context: Context data
    :param text: Button text, default 'Search'
    :param icon: Button icon, default `times <http://fontawesome.io/icon/times/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-waning`
    :param data_dismiss: Adds ``data-dismiss`` with `True` value
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    return btn_button(context, text=text, icon=icon, icon_position=icon_position, btn_css_color=btn_css_color,
                      data_dismiss=data_dismiss, **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_login(context, url, text=_('Login'), icon='login', icon_position=IconPosition.RIGHT,
              btn_css_color='btn-default', **kwargs):
    """
    Renders a ``Login`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Login'
    :param icon: Button icon, default `login <http://fontawesome.io/icon/login/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-default`
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    return btn_button(context, url=url, text=text, icon=icon, icon_position=icon_position,
                      btn_css_color=btn_css_color, **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_logout(context, url, text=_('Logout'), icon='logout', icon_position=IconPosition.RIGHT,
               btn_css_color='btn-default', **kwargs):
    """
    Renders a ``Logout`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Logout'
    :param icon: Button icon, default `logout <http://fontawesome.io/icon/logout/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-default`
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    return btn_button(context, url=url, text=text, icon=icon, icon_position=icon_position,
                      btn_css_color=btn_css_color, **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_update(context, url, text=_('Update'), icon='pencil', icon_position=IconPosition.RIGHT,
               btn_css_color='btn-warning', **kwargs):
    """
    Renders a ``Update`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Update'
    :param icon: Button icon, default `pencil <http://fontawesome.io/icon/pencil/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-default`
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    return btn_button(context, url=url, text=text, icon=icon, icon_position=icon_position,
                      btn_css_color=btn_css_color, **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_delete(context, url, text, icon='trash', icon_position=IconPosition.RIGHT, btn_css_color='btn-danger',
               **kwargs):
    """
    Renders a ``Delete`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Delete'
    :param icon: Button icon, default `trash <http://fontawesome.io/icon/trash/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-danger`
    :param kwargs: Additional keyword args

    :returns: Render-able dict
    """
    return btn_button(context, url=url, text=text, icon=icon, icon_position=icon_position,
                      btn_css_color=btn_css_color, **kwargs)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_next(context, url, text=_('Next'), btn_css_color='btn-default'):
    """
    Renders a ``Next`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Delete'
    :param btn_css_color: Base button color, default `btn-default`

    :returns: Render-able dict
    """

    logger.debug('btn_next() url = %s', url)
    return btn_button(context, url=url, icon='chevron-right', text=text, icon_position=IconPosition.RIGHT,
                      btn_css_color=btn_css_color)


@register.inclusion_tag('buttons/button.html', takes_context=True)
def btn_previous(context, url, text=_('Previous'), btn_css_color='btn-default'):
    """
    Renders a ``Previous`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Delete'
    :param btn_css_color: Base button color, default `btn-default`

    :returns: Render-able dict
    """
    logger.debug('btn_previous() url = %s', url)
    return btn_button(context, url=url, icon='chevron-left', text=text, icon_position=IconPosition.LEFT,
                      btn_css_color=btn_css_color)


@register.inclusion_tag('buttons/switch-button.html', takes_context=False)
def btn_switch(value, switch_alts, large=True, switch_icons="toggle-on,toggle-off", switch_colors="success,danger",
               switch_url=None, title=None, btn_id=None, **kwargs):
    """
    Renders a switch button. When ckicked, an ajax request is sent to server, and the value is possibly changed.

    :param value: Switchable value
    :param switch_alts: alt texts for the switch
    :param large: If True, a larger button will be displayed
    :param switch_icons: Icons to display, in order "yes, No"
    :param switch_colors: Colors used to display the icon, in order "yes, No"
    :param switch_url: Address to invoke to swirch the value.
    :param title: Main title in the button.
    :param btn_id: Identifier for the button
    :param kwargs: Additional kwargs

    :returns: Render-able dict
    """
    output = {'value': value,
              'switch_icons': switch_icons,
              'switch_colors': switch_colors,
              'switch_alts': switch_alts,
              'large': large,
              'title': title,
              'switch_url': switch_url}
    if btn_id is not None:
        output.update({'id': btn_id})

    data = {}
    for item, value in list(kwargs.items()):
        if item.startswith('data_'):
            data[item[5:]] = value
    if data:
        output.update({'data': data})

    return output


@register.inclusion_tag('buttons/single-button.html', takes_context=False)
def btn_single(icon, color, alt, title=None):
    return {'icon': icon,
            'color': color,
            'alt': alt,
            'title': title}


@register.filter
def expand_data(data):
    """
    Expands a dict containing (key, value) pairs into a serie of data-(key)="(value)" HTML attributes

    .. code::

        data = {'foo': 'bar', 'baz": "qux"}
        {{ data|expand_data }} >> 'data-foo="bar" data-baz="qux"'

    :param data: data dict

    :returns: HTML attributes
    """
    if not data:
        return ''

    output = []
    for key, value in list(data.items()):
        if isinstance(value, bool):
            value = str(value).lower()
        output += 'data-%(k)s="%(v)s"' % {'k': key, 'v': value},
    logger.debug('expand_data(%s) output = %s', data, output)
    return mark_safe(" ".join(output))
