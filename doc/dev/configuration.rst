.. _`configuration`:

Configuration
=============

Chaosinventory uses Pythons `ConfigParser <https://docs.python.org/3/library/configparser.html>`_ for user configuration. The used configuration file may be loaded from different directories.

Chaosinventory always loads the :code:`src/chaosinventory/fallback.cfg` first, which initalizes the empty sections. Every use of configuration data must work with only the fallback data available.
If needed, you must specify fallback data locally in your code using the :code:`config.get('section', 'key', fallback='fallback')`-Syntax. 