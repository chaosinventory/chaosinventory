.. _`configuration`:

Configuration
=============

Chaosinventory uses Pythons `ConfigParser <https://docs.python.org/3/library/configparser.html>`_ for user configuration. The used configuration file may be loaded from different directories.

Every use of configuration data must work with only the fallback data available, without an user-provided configuration file.
If needed, you must specify fallback data locally in your code using the :code:`config.get('section', 'key', fallback='fallback')`-Syntax. 