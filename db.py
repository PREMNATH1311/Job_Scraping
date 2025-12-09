import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client=MongoClient(os.getenv("MONGO_URI"))
db=client['jobdata']
collection=db['jobs']

def insert_unique_job(job_data):
    """Insert only if job URL doesn't exist."""
    existing = collection.find_one({"job_url": job_data["job_url"]})

    if existing:
        return False  # job already exists

    collection.insert_one(job_data)
    return True

def insert_multiple_jobs(jobs_list):
    new_count = 0
    for job in jobs_list:
        if insert_unique_job(job):
            new_count += 1
    return new_count
    



