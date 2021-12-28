.. _`dev_frontend`:

Frontend
========

This is our official fancy stock frontend (TM), which you can use to manage your Chaosinventory.

Getting started
---------------

Prerequisites
^^^^^^^^^^^^^

You should have nodejs installed on your system. Information on how to install nodejs can be found `here <https://nodejs.org/en/>`_.

Installation
^^^^^^^^^^^^

You can get the Chaosinventory frontend up and running by:

1. Changing to the frontend directory

   .. code-block:: bash

      cd src/project-static

2. Installing the dependencies

   .. code-block:: bash

      npm install

3. Running the frontend in developer mode

   .. code-block:: bash

      npm start


Building
--------

Chaosinventory Frontend can be built by executing the following command:

.. code-block:: bash

   npm run build


This will compile and bundle all required assets into a folder named `src/project-static/dist`, which contains all assets needed to serve the application over a web server or CDN.
