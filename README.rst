================
geonode-exchange
================

.. image:: https://codecov.io/gh/boundlessgeo/exchange/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/boundlessgeo/exchange

.. image:: https://travis-ci.org/boundlessgeo/exchange.svg?branch=master
    :target: https://travis-ci.org/boundlessgeo/exchange

geonode-exchange is a django project built on GeoNode.

---------
Run Tests
---------
Steps to run tests locally:

.. code-block:: bash

   pip install pytest-cov
   export DJANGO_SETTINGS_MODULE='exchange.settings'

   # see exchange/settings/test_settings.py
   export PYTEST=1

   python manage.py migrate
   python manage.py collectstatic --noinput
   py.test --ignore=tests/ --cov-report html:cov_html --cov=exchange exchange/tests/
