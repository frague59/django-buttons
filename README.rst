==============
django-buttons
==============

This application provides some simple template tags to insert some buttons into templates

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
   {% home %}



