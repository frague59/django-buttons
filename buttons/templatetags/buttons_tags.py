"""
Template tags to display buttons in pages

:creationdate: 09/01/2017 09:21
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: forms.models
"""

import enum
import logging
import pprint
from typing import Any, Dict, Optional, Union

from django import template
from django.conf import settings
from django.forms.utils import flatatt
from django.utils.safestring import SafeText, mark_safe
from django.utils.translation import gettext as _

logger = logging.getLogger("buttons.templatetags.buttons_tags")

register = template.Library()


def get_filename(filename_template: str = settings.BUTTONS_DEFAULT_TEMPLATE_PATH) -> str:
    """
    Gets the filename according to the presence of fontawesome 5

    :param filename_template: filename template
    :return:
    """
    if settings.BUTTONS_FONTAWESOME_VERSION == 5 or "fontawesome_5" in settings.INSTALLED_APPS:
        logger.info("get_filename() fontawesome_5 detected...")
        return filename_template.format(package="fontawesome-5")

    return filename_template.format(package="fontawesome-4")


class IconPosition(enum.Enum):
    """
    Icon positions enumeration
    """

    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ONLY = "ONLY"
    NONE = "NONE"


class ButtonText(enum.Enum):
    """
    Default texts for buttons
    """

    BACK = _("Back")
    PREVIOUS = _("Previous")
    NEXT = _("Next")
    COPY = _("Copy")
    DOWNLOAD = _("Download")
    LINK = _("Link")
    HOME = _("Home")
    DELETE = _("Delete")
    UPDATE = _("Update")
    CREATE = _("Create")
    LOGIN = _("Login")
    LOGOUT = _("Logout")
    SUBMIT = _("Submit")
    LIST = _("List")
    DETAIL = _("Detail")
    SEARCH = _("Search")


def get_param(key, kwargs, context, default=None):
    """
    Gets the parameter from the kwargs, then from the context and finally returns the default value

    :param key: Name on the parameters
    :param kwargs: Kwargs dict
    :param context: Context dict
    :param default: Default value
    :return: value for the given key
    """

    if kwargs.get(key, None) is not None:
        return kwargs.pop(key)

    if context.get(key, None) is not None:
        return context.get(key)

    return default


def _get_btn_id(context, **kwargs) -> str:
    btn_id = kwargs.pop("id", None) or context.get("id") or kwargs.pop("btn_id", None) or context.get("btn_id")
    logger.debug(f"_get_btn_id() btn_id = {btn_id}")
    return btn_id


def _get_icon_position(context, **kwargs) -> str:
    icon_position = kwargs.pop("icon_position", None) or context.get("icon_position", settings.BUTTONS_ICON_POSITION)

    if isinstance(icon_position, IconPosition):
        icon_position = icon_position.value
    else:
        icon_position = IconPosition(icon_position).value
    logger.debug(f"_get_icon_position() btn_id = {icon_position}")
    return icon_position


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_button(
    context,
    **kwargs,
) -> Dict[str, Any]:
    """
    Displays a default button

    :param context: Context data
    :param kwargs: Additional keyword args in:

    + `text`: Button text, default 'Button'
    + `title`: alternative title, used for tooltips for example
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

    :return: Render-able dict
    """
    # logger.debug('btn_button() kwargs = %s', kwargs)

    text = kwargs.pop("text", None) or context.get("text")
    title = kwargs.pop("title", None) or context.get("title")
    url = kwargs.pop("url", None) or context.get("url")
    _type = get_param("btn_type", kwargs, context, "button")
    btn_id = _get_btn_id(context, **kwargs)

    btn_name = kwargs.pop("btn_name", None) or kwargs.pop("name", None)
    btn_value = kwargs.pop("btn_value", None) or kwargs.pop("value", None)

    icon = kwargs.pop("icon", None) or context.get(
        "icon",
        settings.BUTTONS_ICON,
    )

    icon_position = _get_icon_position(context, **kwargs)

    icon_css_extra = kwargs.pop("icon_css_extra", None) or context.get(
        "icon_css_extra",
        settings.BUTTONS_ICON_CSS_EXTRA,
    )
    btn_css_color = kwargs.pop("btn_css_color", None) or context.get(
        "btn_css_color",
        settings.BUTTONS_BTN_CSS_COLOR,
    )
    btn_css_extra = kwargs.pop("btn_css_extra", None) or context.get(
        "btn_css_extra",
        settings.BUTTONS_BTN_CSS_EXTRA,
    )

    # data-* items
    data_dismiss = kwargs.pop("data_dismiss", None) or context.get("data_dismiss")
    data_toggle = kwargs.pop("data_toggle", None) or context.get("data_toggle")
    data_target = kwargs.pop("data_target", None) or context.get("data_target")
    data_placement = kwargs.pop("data_placement", None) or context.get("data_placement")

    # Dict initialization
    output = {
        "text": text,
        "url": url,
        "name": btn_name,
        # tooltip
        "tooltip": title,
        # icon informations
        "icon": icon,
        "icon_position": icon_position,
        "icon_css_extra": icon_css_extra,
        # btn informations
        "btn_css_color": btn_css_color,
        "btn_css_extra": btn_css_extra,
        "btn_type": _type,
        "btn_id": btn_id,
        # `data-*` fields
        "data_dismiss": data_dismiss,
        "data_toggle": data_toggle,
        "data_target": data_target,
        "data_placement": data_placement,
        "debug": settings.DEBUG,
    }
    if kwargs:
        output.update(
            {"flatatt": flatatt(kwargs)},
        )

    if btn_value:
        output.update({"value": btn_value})

    logger.debug(f"btn_button() output = {pprint.pformat(output, indent=2)}")

    return output


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_copy(
    context,
    url,
    text=ButtonText.COPY.value,
    icon="copy",
    icon_position=IconPosition.RIGHT,
    **kwargs,
) -> Dict[str, Any]:
    """
    Displays a ``copy`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Download'
    :param icon: Button icon, default `copy <http://fontawesome.io/icon/copy/>`
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param kwargs: Additional keyword args in:

    + `btn_css_class`: Button bootstrap class

    :return: Render-able dict
    """
    return btn_button(
        context,
        url=url,
        text=text,
        icon=icon,
        icon_position=icon_position,
        **kwargs,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_download(
    context,
    url,
    text=ButtonText.DOWNLOAD.value,
    icon="download",
    icon_position=IconPosition.RIGHT,
    **kwargs,
) -> Dict[str, Any]:
    """
    Displays a ``download`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Download'
    :param icon: Button icon, default `download <http://fontawesome.io/icon/download/>`
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param kwargs: Additional keyword args in:

    + `btn_css_class`: Button bootstrap class

    :return: Render-able dict
    """
    return btn_button(
        context,
        url=url,
        text=text,
        icon=icon,
        icon_position=icon_position,
        **kwargs,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_back(
    context,
    text=ButtonText.BACK.value,
    icon="chevron-left",
    icon_position=IconPosition.LEFT,
    btn_css_color="btn-primary",
    **kwargs,
) -> Dict[str, Any]:
    """
    Displays a ``btn_back`` button

    :param context: Context data
    :param text: Button text, default 'Back'
    :param icon: Button icon, default `chevron-left <http://fontawesome.io/icon/chevron-left/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.LEFT`
    :param btn_css_color: Button css class, default ``btn-primary``
    :param kwargs: Additional keyword args in:

    + `btn_css_class`: Button bootstrap class

    :return: Render-able dict
    """
    return btn_button(
        context,
        text=text,
        icon=icon,
        icon_position=icon_position,
        btn_css_color=btn_css_color,
        url="javascript:history.back()",
        **kwargs,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_link(
    context,
    url,
    text=ButtonText.LINK.value,
    icon="link",
    icon_position=IconPosition.RIGHT,
    btn_css_color="btn-default",
    **kwargs,
) -> Dict[str, Any]:
    """
    Displays a simple ``link`` btn_button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: link text, default 'link'
    :param icon: Icon label, default `link <http://fontawesome.io/icon/link/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.LEFT`
    :param btn_css_color: Button bootstrap class, default 'btn-default'

    :param kwargs:

    :return: Render-able dict
    """
    return btn_button(
        context,
        url=url,
        text=text,
        icon=icon,
        icon_position=icon_position,
        btn_css_color=btn_css_color,
        **kwargs,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_home(
    context,
    url: str = "/",
    text: str = ButtonText.HOME.value,
    icon: str = "home",
    icon_position: Union[IconPosition, str] = IconPosition.LEFT,
    btn_css_color="btn-primary",
    **kwargs,
) -> Dict[str, Any]:
    """
    Displays a ``btn_back`` btn_button

    :param context: Context data
    :param url: Target URL, default '/'
    :param text: Button text, default 'Home'
    :param icon: Button icon, default `home <http://fontawesome.io/icon/home/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.LEFT`
    :param btn_css_color: Button bootstrap class, default 'btn-primary'
    :param kwargs: Additional keyword args

    :return: Render-able dict
    """
    return btn_button(
        context,
        url=url,
        text=text,
        icon=icon,
        icon_position=icon_position,
        btn_css_color=btn_css_color,
        **kwargs,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_submit(
    context,
    text=ButtonText.SUBMIT.value,
    icon="check",
    icon_position=IconPosition.RIGHT,
    btn_css_color="btn-primary",
    **kwargs,
) -> Dict[str, Any]:
    """
    Displays a ``submit`` button

    :param context: Context data
    :param text: Button text, default 'Submit'
    :param icon: Button icon, default `check <http://fontawesome.io/icon/check/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color
    :param kwargs: Additional keyword args

    :return: Render-able dict
    """
    return btn_button(
        context,
        text=text,
        btn_type="submit",
        icon=icon,
        btn_css_color=btn_css_color,
        icon_position=icon_position,
        **kwargs,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_list(
    context,
    url,
    text=ButtonText.LIST.value,
    icon="list",
    icon_position=IconPosition.RIGHT,
    btn_css_color="btn-primary",
    **kwargs,
) -> Dict[str, Any]:
    """
    Displays a ``list`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Submit'
    :param icon: Button icon, default `list <http://fontawesome.io/icon/list/>`
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color
    :param kwargs: Additional keyword args

    :return: Render-able dict
    """
    return btn_button(
        context, url=url, text=text, icon=icon, icon_position=icon_position, btn_css_color=btn_css_color, **kwargs
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_detail(
    context,
    url,
    text=ButtonText.DETAIL.value,
    icon="info",
    icon_position=IconPosition.RIGHT,
    btn_css_color="btn-primary",
    **kwargs,
) -> Dict[str, Any]:
    """
    Displays a `Detail` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Submit'
    :param icon: Button icon, default `info <http://fontawesome.io/icon/info/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.LEFT`
    :param btn_css_color: Base button color
    :param kwargs: Additional keyword args

    :return: Render-able dict
    """
    return btn_button(
        context,
        url=url,
        text=text,
        icon=icon,
        icon_position=icon_position,
        btn_css_color=btn_css_color,
        **kwargs,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_create(
    context,
    url,
    text=ButtonText.CREATE.value,
    icon="plus",
    icon_position=IconPosition.RIGHT,
    btn_css_color="btn-primary",
    **kwargs,
) -> Dict[str, Any]:
    """
    Displays a `Create` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Create'
    :param icon: Button icon, default `plus <http://fontawesome.io/icon/plus/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-primary`
    :param kwargs: Additional keyword args

    :return: Render-able dict
    """
    logger.debug("btn_create() url = *%s*", url)
    return btn_button(
        context,
        url=url,
        text=text,
        icon=icon,
        icon_position=icon_position,
        btn_css_color=btn_css_color,
        **kwargs,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_search(
    context,
    text=ButtonText.SEARCH.value,
    icon="search",
    icon_position=IconPosition.RIGHT,
    btn_css_color="btn-default",
    **kwargs,
) -> Dict[str, Any]:
    """
    Renders a `Search` button

    :param context: Context data
    :param text: Button text, default 'Search'
    :param icon: Button icon, default `search <http://fontawesome.io/icon/search/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-default`
    :param kwargs: Additional keyword args

    :return: Render-able dict
    """
    return btn_button(
        context,
        type="submit",
        text=text,
        icon=icon,
        icon_position=icon_position,
        btn_css_color=btn_css_color,
        **kwargs,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_close(
    context,
    text,
    icon="times",
    icon_position=IconPosition.RIGHT,
    btn_css_color="btn-warning",
    data_dismiss=True,
    **kwargs,
) -> Dict[str, Any]:
    """
    Renders a `Close` button

    :param context: Context data
    :param text: Button text, default 'Search'
    :param icon: Button icon, default `times <http://fontawesome.io/icon/times/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-waning`
    :param data_dismiss: Adds ``data-dismiss`` with `True` value
    :param kwargs: Additional keyword args

    :return: Render-able dict
    """
    return btn_button(
        context,
        text=text,
        icon=icon,
        icon_position=icon_position,
        btn_css_color=btn_css_color,
        data_dismiss=data_dismiss,
        **kwargs,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_login(
    context,
    url,
    text=ButtonText.LOGIN.value,
    icon="login",
    icon_position=IconPosition.RIGHT,
    btn_css_color="btn-default",
    **kwargs,
) -> Dict[str, Any]:
    """
    Renders a ``Login`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Login'
    :param icon: Button icon, default `login <http://fontawesome.io/icon/login/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-default`
    :param kwargs: Additional keyword args

    :return: Render-able dict
    """
    return btn_button(
        context,
        url=url,
        text=text,
        icon=icon,
        icon_position=icon_position,
        btn_css_color=btn_css_color,
        **kwargs,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_logout(
    context,
    url,
    text=ButtonText.LOGOUT.value,
    icon="logout",
    icon_position=IconPosition.RIGHT,
    btn_css_color="btn-default",
    **kwargs,
) -> Dict[str, Any]:
    """
    Renders a ``Logout`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Logout'
    :param icon: Button icon, default `logout <http://fontawesome.io/icon/logout/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-default`
    :param kwargs: Additional keyword args

    :return: Render-able dict
    """
    return btn_button(
        context, url=url, text=text, icon=icon, icon_position=icon_position, btn_css_color=btn_css_color, **kwargs
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_update(
    context,
    url,
    text=ButtonText.UPDATE.value,
    icon="edit",
    icon_position=IconPosition.RIGHT,
    btn_css_color="btn-warning",
    **kwargs,
) -> Dict[str, Any]:
    """
    Renders a ``Update`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Update'
    :param icon: Button icon, default `pencil <http://fontawesome.io/icon/pencil/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-default`
    :param kwargs: Additional keyword args

    :return: Render-able dict
    """
    return btn_button(
        context,
        url=url,
        text=text,
        icon=icon,
        icon_position=icon_position,
        btn_css_color=btn_css_color,
        **kwargs,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_delete(
    context,
    url,
    text=ButtonText.DELETE.value,
    icon="trash",
    icon_position=IconPosition.RIGHT,
    btn_css_color="btn-danger",
    **kwargs,
) -> Dict[str, Any]:
    """
    Renders a ``Delete`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Delete'
    :param icon: Button icon, default `trash <http://fontawesome.io/icon/trash/>`_
    :param icon_position: Button icon position, default :attr:`buttons.templatetags.buttons_tags.IconPosition.RIGHT`
    :param btn_css_color: Base button color, default `btn-danger`
    :param kwargs: Additional keyword args

    :return: Render-able dict
    """
    return btn_button(
        context,
        url=url,
        text=text,
        icon=icon,
        icon_position=icon_position,
        btn_css_color=btn_css_color,
        **kwargs,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_next(
    context,
    url,
    text=ButtonText.NEXT.value,
    btn_css_color="btn-default",
) -> Dict[str, Any]:
    """
    Renders a ``Next`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Delete'
    :param btn_css_color: Base button color, default `btn-default`

    :return: Render-able dict
    """

    logger.debug("btn_next() url = %s", url)
    return btn_button(
        context,
        url=url,
        icon="chevron-right",
        text=text,
        icon_position=IconPosition.RIGHT,
        btn_css_color=btn_css_color,
    )


@register.inclusion_tag(get_filename(), takes_context=True)
def btn_previous(
    context,
    url,
    text=ButtonText.PREVIOUS.value,
    btn_css_color="btn-default",
) -> Dict[str, Any]:
    """
    Renders a ``Previous`` button

    :param context: Context data
    :param url: **Mandatory** target url
    :param text: Button text, default 'Delete'
    :param btn_css_color: Base button color, default `btn-default`

    :return: Render-able dict
    """
    logger.debug("btn_previous() url = %s", url)
    return btn_button(
        context,
        url=url,
        icon="chevron-left",
        text=text,
        icon_position=IconPosition.LEFT,
        btn_css_color=btn_css_color,
    )


@register.inclusion_tag(get_filename("buttons/%s/switch-button.html"), takes_context=False)
def btn_switch(
    value: Any,
    switch_alts: str,
    large: bool = True,
    switch_icons: str = "toggle-on,toggle-off",
    switch_colors: str = "success,danger",
    switch_url: Optional[str] = None,
    title: Optional[str] = None,
    btn_id: Optional[str] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Renders a switch button. When clicked, an ajax request is sent to server, and the value is possibly changed.

    .. note::
        A custom check button is displayed with the `buttons/switch-button.html` template

    :param value: Switchable value
    :param switch_alts: alt texts for the switch
    :param large: If True, a larger button will be displayed
    :param switch_icons: Icons to display, in order "yes, No"
    :param switch_colors: Colors used to display the icon, in order "yes, No"
    :param switch_url: Address to invoke to swirch the value.
    :param title: Main title in the button.
    :param btn_id: Identifier for the button
    :param kwargs: Additional kwargs

    :return: Render-able dict
    """
    output = {
        "value": value,
        "switch_icons": switch_icons,
        "switch_colors": switch_colors,
        "switch_alts": switch_alts,
        "large": large,
        "title": title,
        "switch_url": switch_url,
    }
    if btn_id is not None:
        output.update({"id": btn_id})

    data = {}
    for item, value in list(kwargs.items()):
        if item.startswith("data_"):
            data[item[5:]] = value
    if data:
        output.update({"data": data})

    logger.debug(f"btn_switch() output = {pprint.pformat(output, indent=2)}")
    return output


@register.inclusion_tag(get_filename("buttons/%s/single-button.html"), takes_context=False)
def btn_single(
    icon,
    color,
    alt,
    title=None,
) -> Dict[str, Any]:

    output = {
        "icon": icon,
        "color": color,
        "alt": alt,
        "title": title,
    }
    logger.debug(f"btn_single() output = {pprint.pformat(output, indent=2)}")
    return output


@register.filter
def expand_data(data) -> SafeText:
    """
    Expands a dict containing (key, value) pairs into a serie of data-(key)="(value)" HTML attributes

    .. code::

        data = {'foo': 'bar', 'baz": "qux"}
        {{ data|expand_data }} >> 'data-foo="bar" data-baz="qux"'

    :param data: data dict

    :return: HTML attributes
    """
    if not data:
        return ""

    output = []
    for key, value in list(data.items()):
        if isinstance(value, bool):
            value = str(value).lower()
        output.append(
            f'data-{key}="{value}"',
        )
    logger.debug("expand_data(%s) output = %s", data, output)
    return mark_safe(" ".join(output))
