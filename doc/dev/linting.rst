.. _`linting`:

Code quality and linting
========================

Introduction
------------

Our goal is to have readable and consistent code, our definition of that
is to respect `PEP 8`_ guidelines. The application of the guidelines can
be ignored in especially one case, which is also specified in PEP 8:

   When applying the guideline would make the code less readable, even for someone who is used to reading code that follows this PEP.

Furthermore, to have consistent imports (e.g. relative references, line
wrapping) we sort them using `isort`_, as configured in the :code:`setup.cfg`.

.. attention::
   Please quality-check all your contributions before submitting using the provided script!

Checking your code
------------------

For convenience, a :code:`lint.py` script is located in :code:`/scripts/`.
It does **no** automatic fixing with isort by default. To invoke
the script, simply run

.. code:: bash

   $ python3 scripts/lint.py
   $ scripts/lint.py # Alternative execution as a binary


By adding the :code:`--fix` flag, this tool tries to fix your isort
issues where possible.

Furthermore, it can be run as a git pre-commit hook like so:

.. code:: bash

   $ ln scripts/pre-commit-hook.sh .git/hooks/pre-commit
   $ chmod +x .git/hooks/pre-commit

 
Individual tests
________________

Individual tests can be run using the :code:`--checks` parameter. Multiple
checks can be separated by spaces.

.. code-block:: bash
  
  $ ./lint.py --checks django
  Will run django
  running django...

  System check identified no issues (0 silenced).
  => passed

  Summary:	passed
  django		passed

  $ ./lint.py --checks django isort
  System check identified no issues (0 silenced).
  Will run django, isort
  running django...

  => passed

  running isort...

  => passed

  passed
  django	passed
  isort		passed


Checking manually
-----------------

To check our code against PEP 8 conformity, we use flake8. To check your
code, execute the following command from within the :code:`src` folder:

.. code:: bash

   $ flake8 . --show-source

If there are any violations, those will be listed in combination with their
location.

Check for import errors with the isort command like this:

.. code:: bash

   $ isort --color --check -q .

Again, no output is a good thing as everything is fine. isort, unlike
flake8 can also fix it up for you:

.. code:: bash

   $ isort --interactive .

.. note::

   If you just want to have it fixed without approval of every change,
   leave out the :code:`--interactive`

These tools are also used in our CI, checking every commit and PR for
conformity.

.. _PEP 8: https://legacy.python.org/dev/peps/pep-0008/
.. _isort: https://pycqa.github.io/isort/
.. _flake8: https://flake8.pycqa.org/en/latest/
