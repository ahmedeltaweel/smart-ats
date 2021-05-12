from __future__ import absolute_import, unicode_literals

from celery import shared_task
from pyresparser import ResumeParser


@shared_task
def add(x, y):
    return x + y


@shared_task
def cv(pdf):
    data = ResumeParser(pdf).get_extracted_data()

    for key, value in data.items():
        print(key, ":", value)
    return data
