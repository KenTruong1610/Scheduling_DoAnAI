class Metrics:
    @staticmethod
    def calculate_makespan(machines):
        return max(m.get_finish_time() for m in machines)

    @staticmethod
    def count_late_jobs(jobs):
        late = 0
        for job in jobs:
            if job.finish_time is not None and job.finish_time > job.deadline:
                late += 1
        return late

    @staticmethod
    def average_delay(jobs):
        total = 0
        for job in jobs:
            if job.finish_time > job.deadline:
                total += job.finish_time - job.deadline
        return total / len(jobs)

    @staticmethod
    def evaluate(jobs, machines):
        return {
            "makespan": Metrics.calculate_makespan(machines),
            "late_jobs": Metrics.count_late_jobs(jobs),
            "avg_delay": Metrics.average_delay(jobs)
        }
