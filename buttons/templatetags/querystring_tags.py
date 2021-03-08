"""
Template tags to create smart querystrings

:creationdate: 30/03/17 10:31
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: buttons.templatetags.querystring_tags

"""


import logging
import re

from django import template
from django.http import QueryDict
from django.utils.encoding import smart_str

__author__ = "fguerin"
logger = logging.getLogger("buttons.templatetags.querystring_tags")
register = template.Library()


@register.tag
def query_string(parser, token):
    """
    Template tag for creating and modifying query strings.

    Syntax:
        {% query_string  [<base_querystring>] [modifier]* [as <var_name>] %}

        modifier is <name><op><value> where op in {=, +, -}

    Parameters:
        - base_querystring: literal query string, e.g. '?tag=python&tag=django&year=2011',
                            or context variable bound to either
                            - a literal query string,
                            - a python dict with potentially lists as values, or
                            - a django QueryDict object
                            May be '' or None or missing altogether.
        - modifiers may be repeated and have the form <name><op><value>.
                           They are processed in the order they appear.
                           name is taken as is for a parameter name.
                           op is one of {=, +, -}.
                           = replace all existing values of name with value(s)
                           + add value(s) to existing values for name
                           - remove value(s) from existing values if present
                           value is either a literal parameter value
                             or a context variable. If it is a context variable
                             it may also be bound to a list.
        - as <var name>: bind result to context variable instead of injecting in output
                         (same as in url tag).

    Examples:
    1.  {% query_string  '?tag=a&m=1&m=3&tag=b' tag+'c' m=2 tag-'b' as myqs %}

        Result: myqs == '?m=2&tag=a&tag=c'

    2.  context = {'qs':   {'tag': ['a', 'b'], 'year': 2011, 'month': 2},
                   'tags': ['c', 'd'],
                   'm': 4,}

        {% query_string qs tag+tags month=m %}

        Result: '?tag=a&tag=b&tag=c&tag=d&year=2011&month=4
    """
    # matches 'tagname1+val1' or 'tagname1=val1' but not 'anyoldvalue'
    mod_re = re.compile(r"^(\w+)(=|\+|-)(.*)$")
    bits = token.split_contents()
    query_dict = None
    mods = []
    as_var = None
    bits = bits[1:]
    if len(bits) >= 2 and bits[-2] == "as":
        as_var = bits[-1]
        bits = bits[:-2]
    if len(bits) >= 1:
        first = bits[0]
        if not mod_re.match(first):
            query_dict = parser.compile_filter(first)
            bits = bits[1:]
    for bit in bits:
        match = mod_re.match(bit)
        if not match:
            raise template.TemplateSyntaxError("Malformed arguments to query_string tag")
        name, op, value = match.groups()
        mods.append((name, op, parser.compile_filter(value)))
    return QueryStringNode(query_dict, mods, as_var)


class QueryStringNode(template.Node):
    def __init__(self, query_dict, mods, as_var):
        self.query_dict = query_dict
        self.mods = mods
        self.as_var = as_var

    def render(self, context):
        mods = [(smart_str(k, "ascii"), op, v.resolve(context)) for k, op, v in self.mods]
        if self.query_dict:
            qdict = self.query_dict.resolve(context)
        else:
            qdict = None
        # Internally work only with QueryDict
        qdict = self._get_initial_query_dict(qdict)
        # assert isinstance(query_dict, QueryDict)
        for k, op, v in mods:
            qdict.setlist(k, self._process_list(qdict.getlist(k), op, v))
        qstring = qdict.urlencode()
        if qstring:
            qstring = "?" + qstring
        if self.as_var:
            context[self.as_var] = qstring
            return ""
        else:
            return qstring

    @staticmethod
    def _get_initial_query_dict(query_dict):
        if not query_dict:
            return QueryDict(None, mutable=True)

        if isinstance(query_dict, QueryDict):
            _qdict = query_dict.copy()
            return _qdict

        if isinstance(query_dict, str):
            if query_dict.startswith("?"):
                query_dict = query_dict[1:]
            return QueryDict(query_dict, mutable=True)

        # Accept any old dict or list of pairs.
        try:
            pairs = list(query_dict.items())
        except Exception:  # noqa
            pairs = query_dict

        query_dict = QueryDict(None, mutable=True)

        # Enter each pair into QueryDict object:
        try:
            for key, val in pairs:
                # Convert values to unicode so that detecting
                # membership works for numbers.
                if isinstance(val, (list, tuple)):
                    for e in val:
                        query_dict.appendlist(key, str(e))
                else:
                    query_dict.appendlist(key, str(val))
        except Exception:  # noqa
            pass
        return query_dict

    @staticmethod
    def _process_list(current_list, op, val):
        if not val:
            if op == "=":
                return []
            else:
                return current_list

        # Deal with lists only.
        if not isinstance(val, (list, tuple)):
            val = [val]
        val = [str(v) for v in val]

        # Remove
        if op == "-":
            for v in val:
                while v in current_list:
                    current_list.remove(v)
            return current_list

        # Replace
        if op == "=":
            current_list = val
            return current_list

        # Add
        if op == "+":
            for v in val:
                current_list.append(v)
            return current_list
