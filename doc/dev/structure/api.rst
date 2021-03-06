.. _`api_structure`:


API Structure
=============

.. todo:: Authentication

The API is implemented via the `django rest framework`_.
Using `viewsets`_, most models are serialized and presented at the
:code:`/api/` endpoint. There a browseable API is presented but also in
json format (depending on the requested content-type or if `.json` is
appended).

Viewsets can be very simple, but also quite extendable. If needed,
a lower-level approach could also be taken. However, it is recommended
to use viewsets and other higher abstractions as much as possible to
keep the paths consistent.

Currently, we have the following paths for different models:

.. code-block:: json

   {
    "tag": "/api/tag/",
    "datatype": "/api/datatype/",
    "locationdata": "/api/locationdata/",
    "entity": "/api/entity/",
    "location": "/api/location/",
    "product": "/api/product/",
    "item": "/api/item/"
  }

The API supports both reading and writing. Items can be listed and created
through GET and POST, obtaining details, updating and deletion of can be
done trough GET, PUT, PATH, and DELETE http requests. For now, please refer
to the `drf documentation on making requests`_ and on `generic viewsets`_.

A openapi compatible schema description can be generated using

.. code-block:: shell

   $ python manage.py generateschema --format openapi > schema.yml

.. _django rest framework: https://www.django-rest-framework.org/
.. _viewsets: https://www.django-rest-framework.org/api-guide/viewsets/
.. _drf documentation on making requests: https://www.django-rest-framework.org/api-guide/testing/#making-requests
.. _generic viewsets: https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes
