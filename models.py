# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from geospaas.catalog.models import Dataset as CatalogDataset
from argo_floats.managers import ArgoFloatsManager

class ArgoFloats(CatalogDataset):
    class Meta:
        proxy = True
    objects = ArgoFloatsManager()


# Create your models here.
