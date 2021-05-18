from config.celery_app import app
from pyresparser import ResumeParser
import urllib
import os
from .models import JobApplication


@app.task
def cv(url, job_id):
    job_applications = JobApplication.objects.filter(job_id=job_id)
    for job_application in job_applications:
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
        job_application.data = data
        job_application.save()
        # return data
