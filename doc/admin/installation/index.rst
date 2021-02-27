.. _`installation`:

Installation guide
==================

.. warning::

   The project is currently in pre-alpha state. This setup documentation
   is rudimentary at best and definitely not suited for production.

   Setup instructions will change in future, installation methods may come
   and go. Please always refer to the documentation of the version you
   are installing!

   Help in the development is always appreciated, head over to `GitHub`_
   for a list of open issues!


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

Install and configure Chaosinventory
------------------------------------

Chaosinventory can currently only be installed via pip from the source code as shown below.

.. code-block:: bash

   (venv) $ pip install https://github.com/chaosinventory/chaosinventory/archive/main.tar.gz#subdirectory=src gunicorn
   ...
   Successfully installed Django-3.1.5 chaosinventory-0.0.0 gunicorn-20.0.4

Now we need to provide a configuration for chaosinventory. This can be
located in multiple locations (in the order of preference, first found
will be used):

* The path specified in the Environment variable :code:`CHAOSINVENTORY_CONFIG_FILE`
* The :code:`chaosinventory.cfg` in your curent working directory
* :code:`/etc/chaosinventory/chaosinventory.cfg`

.. todo::

   Improve documentation of the config file.

The example configuration looks like this and, except for **changing the secret**,
should work out of the box using a sqlite Database, however this is not
recommended for production use.

.. code:: ini

  [django]
  secret = foobar2342
  debug = True
  allowed_hosts = *
  language_code = en-us
  time_zone = UTC

  [database]
  engine = sqlite3
  name = db.sqlite3
  user =
  password =
  host =
  port =

  [email]
  backend = filebased.EmailBackend
  host =
  port =
  user =
  password =
  ssl = False
  tls = False

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
.. _GitHub: https://github.com/chaosinventory/chaosinventory/issues
