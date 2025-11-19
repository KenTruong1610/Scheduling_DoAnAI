class Metrics:
    @staticmethod
    def calculate_makespan(machines):
        """Tính makespan - thời gian hoàn thành tất cả jobs"""
        max_time = 0
        for m in machines:
            if m.schedule:  # Nếu máy có jobs
                max_time = max(max_time, m.schedule[-1][2])  # finish time của job cuối
        return max_time

    @staticmethod
    def count_late_jobs(jobs):
        """Đếm số job trễ deadline"""
        late = 0
        for job in jobs:
            if job.finish_time is not None and job.deadline is not None:
                if job.finish_time > job.deadline:
                    late += 1
        return late

    @staticmethod
    def average_delay(jobs):
        """Tính độ trễ trung bình"""
        total = 0
        count = 0
        for job in jobs:
            if job.finish_time is not None and job.deadline is not None:
                if job.finish_time > job.deadline:
                    total += job.finish_time - job.deadline
                    count += 1
        return total / count if count > 0 else 0

    @staticmethod
    def evaluate(jobs, machines):
        """Đánh giá tổng thể"""
        return {
            "makespan": Metrics.calculate_makespan(machines),
            "late_jobs": Metrics.count_late_jobs(jobs),
            "avg_delay": Metrics.average_delay(jobs)
        }