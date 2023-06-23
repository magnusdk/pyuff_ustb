pyuff_ustb: An implementation of USTB's ultrasound file format (UFF) in Python.
===============================================================================

``pyuff_ustb`` is USTB's ultrasound file format (UFF) format in Python. UFF is a dataformat that represents ultrasound data. It can be used to store the raw channel-data that is used to beamform an image, the scan/pixel-grid setup, data that has already been beamformed, and more.

Note that this project only implements USTB's version of UFF, which is considered version ``0.0.1``. Multiple versions of UFF exists, for example check out `uff-reader <https://github.com/waltsims/uff-reader>`_. However, if you only planning to use USTB's version of UFF then you have come to the right place 🕺

Installation
------------

.. code-block:: bash

   python -m pip install pyuff-ustb

Documentation
-------------

.. toctree::
   :maxdepth: 2

   api-reference
