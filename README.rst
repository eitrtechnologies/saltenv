=======
saltenv
=======

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/

.. todo:: (Set ``todo_include_todos = False`` in ``docs/conf.py`` to hide this)

   What is the purpose of this project? Give a brief sentence or two as your pitch.

About
=====

.. todo:: (Set ``todo_include_todos = False`` in ``docs/conf.py`` to hide this)

   A more detailed description about the project.

   All TODO items on this page are part of the pop template, and should be
   reviewed and replaced with actual content.

   This page is the ``README.rst`` page that appears on a repo site, such as
   GitHub/GitLab, but also is what appears on the PyPI landing page of a published
   python project. Sphinx docs, by default, include the contents of this file
   in the published docs.

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based
implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring
together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/saltstack/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/saltstack/pop/pop-create/>`__

Getting Started
===============

Prerequisites
-------------

* Python 3.6+
* git *(if installing from source, or contributing to the project)*

Installation
------------

.. note::

   If wanting to contribute to the project, and setup your local development
   environment, see the ``CONTRIBUTING.rst`` document in the source repository
   for this project.

If wanting to use ``saltenv``, you can do so by either
installing from PyPI or from source.

Install from PyPI
+++++++++++++++++

.. todo:: (Set ``todo_include_todos = False`` in ``docs/conf.py`` to hide this)

   If package is available via PyPI, include the directions.

   .. code-block:: bash

      pip install saltenv

Install from source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@<your-project-path>/saltenv.git
   cd saltenv

   # Setup venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .

Usage
=====

.. todo:: (Set ``todo_include_todos = False`` in ``docs/conf.py`` to hide this)

   Describe some basic example use case for this plugin.

Examples
--------

.. todo:: (Set ``todo_include_todos = False`` in ``docs/conf.py`` to hide this)

   Provide some example CLI-based commands for users.

.. code-block:: bash

   # Example CLI commands

Common Issues
=============

* If this error is encountered, you might be running on Arch and need to install the ``libxcrypt-compat`` package.

.. code-block:: text

    [230732] Error loading Python lib '/tmp/_MEIAEr7dd/libpython3.7m.so.1.0': dlopen: libcrypt.so.1: cannot open shared object file: No such file or directory


Roadmap
=======

.. todo:: (Set ``todo_include_todos = False`` in ``docs/conf.py`` to hide this)

   Update **open issues** link below with link to GitHub/GitLab/etc. issues page

Reference the `open issues <https://issues.example.com>`__ for a list of
proposed features (and known issues).

Acknowledgements
================

* `Img Shields <https://shields.io>`__ for making repository badges easy.
