Contributing
============

Set Up Your Environment
-----------------------

This project is designed for the Python 3 series... so you'll need to have
that available. To set up everyting else, do the following:

::

  $ mkdir pyPrintful
  $ cd pyPrintful
  $ git clone https://github.com/559Labs/pyPrintful.git .
  $ python3 -m venv env
  $ source env/bin/activate
  $ pip install -r requirements.txt


Build the Documentation
-----------------------

If you set up your project as described above, you should have Sphinx commands
available. So, do the following from the project root folder:

::

  $ cd docs
  $ make html

The rendered files should now be saved in ``./docs/_build/html/``.
