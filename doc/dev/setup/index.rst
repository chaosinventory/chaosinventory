.. _`dev_setup`:

Setup
=====

Get a copy of the source code
-----------------------------

.. code-block:: bash

   $ git clone https://github.com/chaosinventory/chaosinventory.git
   $ cd chaosinventory

Local environment
-----------------

To avoid mixing of dependencies, a virtual environment is highly recommended.

.. code-block:: bash

   $ python3 -m venv venv
   $ source venv/bin/activate

Working on and with the code
----------------------------

The code itself is located within the :code:`src` directory.
See :ref:`directory_structure` for a full documentation on the projects structure.

You will also need to install some requirements using pip.

.. code-block:: bash

   (venv) $ cd src/
   (venv) $ pip install -r requirements.txt

To populate your local development database you must execute the migrations.

.. code-block:: bash

   (venv) $ ./manage.py migrate

Development server
------------------

To run the project and visit it in your browser, django ships a small test server.

.. code-block:: bash

   (venv) $ ./manage runserver -6

.. note::

   Do not forget the :code:`-6` in order to only use proper internet
   protocols and not bother with legacy stuff.

You can now visit :code:`http://[::1]:8000/` in your browser.
