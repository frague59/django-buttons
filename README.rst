|pipeline status|

django-buttons
==============

This application provides some simple template tags to insert some
buttons into templates.

-  Documentation technique :
   https://fguerin.docs.tourcoing.fr/django-buttons/

Installation
------------

Install application with pypi:

.. code:: sh

    $ pip install django-buttons

Add application to your INSTALLED\_APPS:

.. code:: python

    INSTALLED_APPS = [
    ...
    'buttons',
    ...
    ]

Use buttons in your templates
-----------------------------

.. code:: html

    {% load buttons_tags %}
    ...
    {% btn_home %}

Buttons can have some parameters :

-  \`url\`: target url
-  \`title\`: displayed text
-  \`icon\`: fa aware name, ie. 'home' for
   `fa-home <http://fontawesome.io/icon/home/>`__

-  \`icon\_position\`: Position of the icon, 'right', 'left' or 'none'
   (no icon displayed) ...

**Enjoy !**

.. |pipeline status| image:: http://gitlab.ville.tg/fguerin/django-buttons/badges/master/pipeline.svg
   :target: http://gitlab.ville.tg/fguerin/django-buttons/commits/master
