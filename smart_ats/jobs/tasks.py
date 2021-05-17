from celery import shared_task
# from config.celery_app import app
from pyresparser import ResumeParser
import urllib
import os
from .models import JobApplication


@shared_task
def cv(url):
    response = urllib.request.urlopen(url)
    if url[-3:] == 'pdf':
        file = open("resume.pdf", 'wb')
        file.write(response.read())
        file.close()
        data = ResumeParser("resume.pdf").get_extracted_data()
        os.remove("resume.pdf")
    else:
        file = open("resume.txt", 'wb')
        file.write(response.read())
        file.close()
        data = ResumeParser("resume.txt").get_extracted_data()
        os.remove("resume.txt")
    JobApplication.data = data
    JobApplication.save()
    return data
