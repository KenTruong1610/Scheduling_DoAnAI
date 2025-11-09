# schedule.py
from job import Job
from machine import Machine

class Schedule:
    """Quản lý lịch làm việc: gán job, đánh giá lịch, tổng hợp dữ liệu"""

    def __init__(self, machines, jobs):
        self.machines = machines  # danh sách đối tượng Machine
        self.jobs = jobs          # danh sách đối tượng Job

    def assign_job(self, job, machine, start_time):
        """Gán job vào máy tại thời điểm start_time"""
        machine.assign(job, start_time)

    def evaluate(self):
        """Tính các chỉ số hiệu năng của lịch"""
        total_makespan = max((m.schedule[-1][2] if m.schedule else 0) for m in self.machines)
        total_lateness = sum(max(0, job.finish_time - job.deadline) 
                             for job in self.jobs if job.deadline is not None)
        return {
            "makespan": total_makespan,
            "total_lateness": total_lateness
        }

    def get_schedule_summary(self):
        """Trả về dữ liệu dạng dict để hiển thị hoặc visualize"""
        summary = {}
        for m in self.machines:
            summary[m.machine_id] = [
                (job.job_id, start, finish) for job, start, finish in m.schedule
            ]
        return summary
