==================
Contributing Guide
==================

Contributions are what make the open source community such an amazing place to
learn, inspire, and create in. Any contributions you make are **greatly appreciated!**

TL;DR Quickstart
================

#. Have pre-requisites completed:

   * ``git``
   * ``nox``
   * ``pre-commit``
   * Python 3.6+

#. Fork the project
#. ``git clone`` your fork locally
#. Create your feature branch (ex. ``git checkout -b amazing-feature``)
#. Setup your local development environment

   .. code-block:: bash

      # setup venv
      python3 -m venv .venv
      source .venv/bin/activate
      pip install -U pip setuptools wheel pre-commit nox

      # pre-commit configuration
      pre-commit install

#. Hack away!
#. Commit your changes (ex. ``git commit -m 'Add some amazing-feature'``)
#. Push to the branch (ex. ``git push origin amazing-feature``)
#. Open a pull request

For the full details, see below.

Ways to contribute
==================

We value all contributions, not just contributions to the code. In addition to
contributing to the code, you can help the project by:

* Writing, reviewing, and revising documentation, modules, and tutorials
* Opening issues on bugs, feature requests, or docs
* Spreading the word about how great this project is

The rest of this guide will explain our toolchain and how to set up your
environment to contribute to the project.


Overview of how to contribute to this repository
================================================

To contribute to this repository, you first need to set up your own local repository:

* `Fork, clone, and branch the repo`_
* `Set up your local preview environment`_

After this initial setup, you then need to:

* `Sync local master branch with upstream master`_
* Edit the documentation in reStructured Text
* `Preview HTML changes locally`_
* Open a PR

Once a merge request gets approved, it can be merged!

Prerequisites
=============

For local development, the following prerequisites are needed:

* `git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`__
* `Python 3.6+ <https://realpython.com/installing-python/>`__
* `Ability to create python venv <https://realpython.com/python-virtual-environments-a-primer/>`__

Windows 10 users
----------------

For the best experience, when contributing from a Windows OS to projects using
Python-based tools like ``pre-commit``, we recommend setting up `Windows Subsystem
for Linux (WSL) <https://docs.microsoft.com/en-us/windows/wsl/>`__, with the
latest version being WSLv2.

The following gists on GitHub have been consulted with success for several
contributors:

* `Official Microsoft docs on installing WSL <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`__

* A list of PowerShell commands in a gist to `Enable WSL and Install Ubuntu 20.04
  <https://gist.github.com/ScriptAutomate/f94cd44dacd0f420fae65414e717212d>`__

  * Ensure you also read the comment thread below the main content for
    additional guidance about using Python on the WSL instance.

We recommend `Installing Chocolatey on Windows 10 via PowerShell w/ Some Starter Packages
<https://gist.github.com/ScriptAutomate/02e0cf33786f869740ee963ed6a913c1>`__.
This installs ``git``, ``microsoft-windows-terminal``, and other helpful tools via
the awesome Windows package management tool, `Chocolatey <https://chocolatey.org/why-chocolatey>`__.

``choco install git`` easily installs ``git`` for a good Windows-dev experience.
From the ``git`` package page on Chocolatey, the following are installed:

* Git BASH
* Git GUI
* Shell Integration

Fork, clone, and branch the repo
================================

This project uses the fork and branch Git workflow. For an overview of this method,
see
`Using the Fork-and-Branch Git Workflow <https://blog.scottlowe.org/2015/01/27/using-fork-branch-git-workflow/>`__.

* First, create a new fork into your personal user space.
* Then, clone the forked repo to your local machine.

  .. code-block:: bash

     # SSH or HTTPS
     git clone <forked-repo-path>/saltenv.git

.. note::

    Before cloning your forked repo when using SSH, you need to create an SSH
    key so that your local Git repository can authenticate to the GitLab remote server.
    See `GitLab and SSH keys <https://docs.gitlab.com/ee/ssh/README.html>`__ for instructions,
    or `Connecting to GitHub with SSH <https://docs.github.com/en/github-ae@latest/github/authenticating-to-github/connecting-to-github-with-ssh>`__.

Configure the remotes for your main upstream repository:

.. code-block:: bash

    # Move into cloned repo
    cd saltenv

    # Choose SSH or HTTPS upstream endpoint
    git remote add upstream git-or-https-repo-you-forked-from

Create new branch for changes to submit:

.. code-block:: bash

    git checkout -b amazing-feature


Set up your local preview environment
=====================================

If you are not on a Linux machine, you need to set up a virtual environment to
preview your local changes and ensure the `prerequisites`_ are met for a Python
virtual environment.

From within your local copy of the forked repo:

.. code-block:: bash

    # Setup venv
    python3 -m venv .venv
    # If Python 3.6+ is in path as 'python', use the following instead:
    # python -m venv .venv

    # Activate venv
    source .venv/bin/activate
    # On Windows, use instead:
    # .venv/Scripts/activate

    # Install required python packages to venv
    pip install -U pip setuptools wheel pre-commit nox
    pip install -r requirements/base.txt

    # Setup pre-commit
    pre-commit install


``pre-commit`` and ``nox`` Setup
--------------------------------

This project uses `pre-commit <https://pre-commit.com/>`__ and
`nox <https://nox.thea.codes/en/stable/>`__ to make it easier for
contributors to get quick feedback, for quality control, and to increase
the chance that your merge request will get reviewed and merged.

``nox`` handles Sphinx requirements and plugins for you, always ensuring your
local packages are the needed versions when building docs. You can think of it
as ``Make`` with superpowers.


What is pre-commit?
-------------------

``pre-commit`` is a tool that will automatically run
local tests when you attempt to make a git commit. To view what tests are run,
you can view the ``.pre-commit-config.yaml`` file at the root of the
repository.

One big benefit of pre-commit is that *auto-corrective measures* can be done
to files that have been updated. This includes Python formatting best
practices, proper file line-endings (which can be a problem with repository
contributors using differing operating systems), and more.

If an error is found that cannot be automatically fixed, error output will help
point you to where an issue may exist.


Sync local master branch with upstream master
=============================================

If needing to sync feature branch with changes from upstream master, do the
following:

.. note::

    This will need to be done in case merge conflicts need to be resolved
    locally before a merge to master in the upstream repo.

.. code-block:: bash

    git checkout master
    git fetch upstream
    git pull upstream master
    git push origin master
    git checkout my-new-feature
    git merge master


Preview HTML changes locally
============================

To ensure that the changes you are implementing are formatted correctly, you
should preview a local build of your changes first. To preview the changes:

.. code-block:: bash

    # Activate venv
    source .venv/bin/activate
    # On Windows, use instead:
    # .venv/Scripts/activate

    # Generate HTML documentation with nox
    nox -e 'docs-html(clean=False)'

    # Sphinx website documentation is dumped to docs/_build/html/*
    # You can view this locally
    # firefox example
    firefox docs/_build/html/index.html

.. note::

    If you encounter an error, Sphinx may be pointing out formatting errors
    that need to be resolved in order for ``nox`` to properly generate the docs.

Testing a ``pop`` project
=========================

.. code-block:: bash

    # View all nox targets
    nox -l

    # Output version of Python activated/available
    # python --version OR
    python3 --version

    # Run appropriate test
    # Ex. if Python 3.8.x
    nox -e 'tests-3.8'

This project is a ``pop`` project which makes use of ``pytest-pop``, a
``pytest`` plugin. For more information on ``pytest-pop``, and writing tests
for ``pop`` projects:

* `pytest-pop README <https://gitlab.com/saltstack/pop/pytest-pop/-/blob/master/README.rst>`__
* `pytest documentation <https://docs.pytest.org/en/stable/contents.html>`__
