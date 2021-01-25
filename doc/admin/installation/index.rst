.. _`installation`:

Installation guide
==================

.. warning::

   The project is currently in pre-alpha state. This setup documentation
   is rudimentary at best and definetly not suited for production. 


Chaosinventory ships as a standalone app. Therefore, you don't need to bring your own django project.
You only need to have a wsgi server such as `gunicorn`_ and a database. `PostgreSQL`_ is recommended.

Venv setup
----------

.. todo:: Separate user

To isolate python applications and their requirements, it is highly
advised to install in a so called `virtual environment`_.

.. code-block:: bash

   $ mkdir chaosinventory
   $ cd chaosinventory
   $ python3 -m venv venv
   $ source venv/bin/activate
   (venv) $ which python # check it is setup correctly
   /path/to/chaosinventory/venv/bin/python

Install Chaosinventory
----------------------

Chaosinventory can currently only be installed via pip from the source code as shown below.

.. code-block:: bash

   (venv) $ pip install https://github.com/chaosinventory/chaosinventory/archive/main.tar.gz#subdirectory=src gunicorn
   ...
   Successfully installed Django-3.1.5 chaosinventory-0.0.0 gunicorn-20.0.4

Before the app can be started, the database structure must be created and
all static files collected.

.. code-block:: bash

   (venv) $ chaosinventory migrate
   Operations to perform:
      Apply all migrations: admin, auth, contenttypes, sessions
   Running migrations:
     Applying contenttypes.0001_initial... OK
     ...
     Applying sessions.0001_initial... OK

   (venv) $ chaosinventory collectstatic
   132 static files copied to '/path/to/chaosinventory/venv/lib/python3.9/site-packages/static'.


.. todo::

   This will place a db.sqlite3 in the venv directory. This is in
   **no way** recommended or stable. This will need to be updated once
   the configuration is in place.

.. todo::

   The statics will also be collected into the venv directory. This
   should also be updated once the configuration is in place.

Start gunicorn
--------------

Gunicorn will server our application for it to be accessible via http.

.. code-block:: bash

   (venv) $ venv/bin/gunicorn chaosinventory.wsgi --name chaosinventory --bind="[::1]:8000"
   [2021-01-23 20:13:45 +0100] [107596] [INFO] Starting gunicorn 20.0.4
   [2021-01-23 20:13:45 +0100] [107596] [INFO] Listening at: http://[::1]:8000 (107596)
   [2021-01-23 20:13:45 +0100] [107596] [INFO] Using worker: sync
   [2021-01-23 20:13:45 +0100] [107597] [INFO] Booting worker with pid: 107597

When visiting http://[::1]:1234/ we will be greeted by hello world page (for now).

.. todo:: Systemd service

.. todo:: nginx configuration with ssl

.. _gunicorn: https://gunicorn.org/
.. _PostgreSQL: https://www.postgresql.org/
.. _virtual environment: https://docs.python.org/3/library/venv.html
