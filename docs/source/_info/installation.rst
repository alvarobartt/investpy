.. _installation-label:

Installation
============

.. note::

    After installing the package you are now available to use it! As investpy's latest release is 1.0.3 the installation is
    optimized for it. If you try installing another investpy release, some features may not work.

First Installation
------------------

In order to get this package working you will need to install it on its last version. To install the package on either way
you will need to have a Python 3.x version installed and pip or conda, so you can install Python packages from PyPI and from Anaconda
Cloud, respectively. So, to install the latest release of `investpy <https://pypi.org/project/investpy/>`_, you can either do it:

* via Python Package Indexer (PyPI)::

    $ python -m pip install investpy

* via Anaconda Cloud::

    $ conda install investpy

* from GitHub via PyPI::

    $ python -m pip install https://github.com/alvarobartt/investpy/archive/master.zip


Update Package
--------------

If you already had `investpy <https://pypi.org/project/investpy/>`_ installed and you want to update it you can do it:

* via PyPI::

    $ python -m pip install --upgrade investpy

* via Anaconda Cloud::

    $ conda update investpy

* from GitHub via PyPi::

    $ python -m pip install --upgrade https://github.com/alvarobartt/investpy/archive/master.zip

All the dependencies are already listed on the setup file of the package, but to sum them up, when installing
`investpy <https://pypi.org/project/investpy/>`_, it will install the following dependencies:

* `pandas 0.25.1 <https://pypi.org/project/pandas/>`_
* `requests 2.22.0 <https://pypi.org/project/requests/>`_
* `lxml 4.4.1 <https://pypi.org/project/lxml/>`_
* `unidecode 1.1.1 <https://pypi.org/project/unidecode/>`_
