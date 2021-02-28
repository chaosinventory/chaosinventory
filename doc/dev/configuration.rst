.. _`configuration`:

Configuration
=============

Chaosinventory uses Pythons `ConfigParser <https://docs.python.org/3/library/configparser.html>`_ for user configuration. The used configuration file may be loaded from different directories.

Chaosinventory always loads the :code:`src/chaosinventory/fallback.cfg` first. Every use of configuration data must work with only the fallback data available.
You may specify fallback data in the fallback.cfg (especially sections), or locally in your code using the :code:`config.get('section', 'key', fallback='fallback')`-Syntax. 

Especially for non-critical configuration keys, the later variant is preferred.