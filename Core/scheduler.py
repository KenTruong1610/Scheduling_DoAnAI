# scheduler.py
from abc import ABC, abstractmethod

class Scheduler(ABC):
    """Lớp trừu tượng (base class) cho các thuật toán sắp xếp lịch"""

    def __init__(self, jobs, machines):
        self.jobs = jobs
        self.machines = machines
        self.best_schedule = None
        self.best_score = float('inf')

    @abstractmethod
    def schedule(self):
        """
        Thực hiện việc sắp xếp lịch.
        Các lớp con (GreedyScheduler, GWOScheduler, ACO...) sẽ override
        """
        pass

    @abstractmethod
    def evaluate(self, schedule):
        """
        Tính hàm mục tiêu (tổng thời gian, độ trễ, chi phí,...)
        Các lớp con sẽ implement dựa vào schedule
        """
        pass
