from __future__ import absolute_import, unicode_literals
from celery import shared_task
import random


# TESTING
@shared_task
def add(x, y):
    return x + y

