# django-geo-spaas-argo-floats
Geo-SPaaS ingestor for Argo floats


Django-Geo-SPaaS - GeoDjango Apps for satellite data management
===========================================================
[![Build Status](https://travis-ci.org/nansencenter/django-geo-spaas-argo-floats.svg?branch=master)](https://travis-ci.org/nansencenter/django-geo-spaas-argo-floats)
[![Coverage Status](https://coveralls.io/repos/github/nansencenter/django-geo-spaas-argo-floats/badge.svg?branch=master)](https://coveralls.io/github/nansencenter/django-geo-spaas-argo-floats)


How to add new data to Geo-SPaaS catalog
----------------------------------------
Install geo-spaas-vagrant:
```
  git clone https://github.com/nansencenter/geo-spaas-vagrant
  cd geo-spaas-vagrant
  vagrant up geospaas_core
```
Connect to the virtual machine and use GeoSPaaS
```
  vagrant ssh geospaas_core
  cd django-geo-spaas/project
  ./manage.py ingest name_of_your_file
