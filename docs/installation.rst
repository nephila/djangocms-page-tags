============
Installation
============

#. Install djangocms-page-tags::

        $ pip install djangocms-page-tags

   or from the repository::

        pip install -e https://github.com/nephila/djangocms-page-tags#egg=djangocms-page-tags

#. Then add it to INSTALLED_APPS along with its dependencies::

        'taggit',
        'taggit_autosuggest',
        'djangocms_page_tags',

#. Add `taggit_autosuggest` to urlconf::

        url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),


#. Synchronize the database with syncdb::

        $ python manage.py syncdb

   or migrate::

        $ python manage.py migrate

#. That's all!

************
Dependencies
************

* `django-taggit`_ >= 0.11
* `django-taggit-autosuggest`_  >= 0.2.1

you may want to install `django-taggit-templatetags`_ for better tag
management in the template.


.. _django-taggit: https://pypi.python.org/pypi/django-taggit
.. _django-taggit-autosuggest: https://pypi.python.org/pypi/django-taggit-autosugges
.. _django-taggit-templatetags: https://pypi.python.org/pypi/django-taggit-templatetags
