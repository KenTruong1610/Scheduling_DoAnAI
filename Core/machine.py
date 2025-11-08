#Lớp đại diện cho một máy trong hệ thống lập lịch dùng để thực hiện các công việc
#Quản lý các công việc đã được gán
# Theo dõi tổng thời gian hoạt động
class Machine:
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.schedule = []  # Danh sách job

    def assign(self, job, start_time):
        self.schedule.append((job, start_time, start_time + job.duration))

    def total_time(self):
        return sum(job.duration for job, _, _ in self.schedule)

    def current_time(self):
        if not self.schedule:
            return 0
        return self.schedule[-1][2]  # Thời gian kết thúc của job cuối cùng