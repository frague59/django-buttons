==============
django-buttons
==============

This application provides some simple template tags to insert some buttons into templates.

+ Documentation : `http://ulysse.ville.tg/docs/django-buttons/ <http://ulysse.ville.tg/docs/django-buttons/>`_

Installation
============

Install application with pypi:

.. code-block:: sh

   $ pip install django-buttons

Add application to your INSTALLED_APPS:

.. code-block:: python

   INSTALLED_APPS = [
   ...
   'buttons',
   ...
   ]

Use buttons in your templates
=============================

.. code-block:: html

   {% load buttons_tags %}
   ...
   {% btn_home %}

Buttons can have some parameters :

+ `url`: target url
+ `title`: displayed text
+ `icon`: fa aware name, ie. 'home' for `fa-home <http://fontawesome.io/icon/home/>`_
+ `icon_position`: Position of the icon, 'right', 'left' or 'none' (no icon displayed)
...


Enjoy
=====



