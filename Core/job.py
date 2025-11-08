#Lớp đại diện cho 1 công việc
class Job:
    def __init__(self, job_id, duration, deadline=None, priority=1):
        self.job_id = job_id
        self.duration = duration
        self.deadline = deadline
        self.priority = priority
        self.start_time= None
        self.finish_time= None

    def set_schedule(self, start_time):
        self.start_time = start_time
        self.finish_time = start_time + self.duration

    def __repr__(self):
        return f"Job {self.job_id}: self.start_time={self.start_time}, finish_time={self.finish_time}"