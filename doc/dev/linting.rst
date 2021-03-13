.. _`linting`:

Code quality and linting
========================

Introduction
------------

Our goal is to have readable and consistent code, our definition of that
is to respect `PEP 8`_ guidelines. The application of these guidelines
have especially one limitation, which is also laid out in the spec and
is practiced by us:

   When applying the guideline would make the code less readable, even for someone who is used to reading code that follows this PEP.

Further more, to have consistent imports (e.g. relative references, line
wrapping) we sort them using `isort`_, as configured in the :code:`setup.cfg`.

Checking your code
------------------

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

These tools are also used in our ci, checking every commit and PR for
conformity.

All in one script
-----------------

For convenience, a :code:`lint.sh` script is located in :code:`/scripts/`.
Whilst it does **no** automatic fixing with isort, it can be run as a git
pre-commit hook like so:

.. code:: bash

   $ ln scripts/lint.sh .git/hooks/pre-commit
   $ chmod +x .git/hooks/pre-commit

Of course, it can be used outside of git hooks to!

.. _PEP 8: https://legacy.python.org/dev/peps/pep-0008/
.. _isort: https://pycqa.github.io/isort/
.. _flake8: https://flake8.pycqa.org/en/latest/
