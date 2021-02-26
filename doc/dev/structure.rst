.. _`directory_structure`:

Directory Structure
===================

Chaosinventory is an entire, (mostly) ready to ship, django application.
Therefore, the structure is just like any django project you may have locally
instead of just being a single app.

All of the source-code itself resides in ``src/`` and is structured like
any other python module. The corresponding ``setup.cfg`` and ``setup.py``
are directly located in this folder.

``chaosinventory/``
  Location of the main module (aka. the django project)

  ``base/``
    The core of chaosinventory, all models and essential methods are located
    here. Basically a :std:doc:`django Application <django:ref/applications>`.
