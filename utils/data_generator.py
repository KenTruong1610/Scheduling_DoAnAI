import random
from Core.job import Job

class DataGenerator:
    @staticmethod
    def generate_jobs(n_jobs, duration_range=(1, 20), deadline_range=(5, 50)):
        jobs = []
        for i in range(n_jobs):
            duration = random.randint(*duration_range)
            deadline = random.randint(*deadline_range)
            priority = random.randint(1, 5)
            job = Job(
                job_id=i + 1,
                duration=duration,
                deadline=deadline,
                priority=priority
            )
            jobs.append(job)
        return jobs
