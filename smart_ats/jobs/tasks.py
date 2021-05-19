from config.celery_app import app
from pyresparser import ResumeParser
import urllib
import os
from .models import JobApplication


@app.task
def cv(url, job_app_id):
    job_application = JobApplication.objects.get(id=job_app_id)
    response = urllib.request.urlopen(url)
    with open("resume." + url[-3:], 'wb') as file:
        file.write(response.read())
    data = ResumeParser("resume." + url[-3:]).get_extracted_data()
    os.remove("resume." + url[-3:])
    job_application.data = data
    job_application.save()
