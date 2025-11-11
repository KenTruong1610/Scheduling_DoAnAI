import copy
from Core.scheduler import Scheduler
from Core.schedule import Schedule

class GreedyScheduler(Scheduler):
    def __init__(self, jobs, machines, strategy="SPT"):
        super().__init__(jobs, machines)
        self.strategy = strategy  # SPT (Shortest Processing Time), EDD (Earliest Due Date), etc.

    def schedule(self):
        # Tạo bản sao để không ảnh hưởng đến dữ liệu gốc
        jobs_copy = copy.deepcopy(self.jobs)
        machines_copy = copy.deepcopy(self.machines)
        
        # Sắp xếp jobs theo chiến lược
        if self.strategy == "SPT":
            jobs_copy.sort(key=lambda x: x.duration)
        elif self.strategy == "EDD":
            jobs_copy = [job for job in jobs_copy if job.deadline is not None]
            jobs_copy.sort(key=lambda x: x.deadline)
        else:  # FCFS (First Come First Served)
            jobs_copy.sort(key=lambda x: x.job_id)
        
        # Gán jobs vào máy có thời gian hoàn thành sớm nhất
        for job in jobs_copy:
            # Tìm máy có thời gian hoàn thành sớm nhất
            best_machine = min(machines_copy, key=lambda m: m.current_time())
            start_time = best_machine.current_time()
            best_machine.assign(job, start_time)
        
        schedule = Schedule(machines_copy, jobs_copy)
        self.best_schedule = schedule
        self.best_score = self.evaluate(schedule)
        
        return schedule

    def evaluate(self, schedule):
        metrics = schedule.evaluate()
        # Hàm mục tiêu: tổ hợp makespan và độ trễ
        return metrics["makespan"] + 0.1 * metrics["total_lateness"]