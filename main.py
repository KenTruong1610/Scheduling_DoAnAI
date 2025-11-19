"""
CHƯƠNG TRÌNH XẾP LỊCH CÔNG VIỆC - ĐỒ ÁN AI
Nhóm 8 - Môn Trí Tuệ Nhân Tạo
Giải thuật: Greedy Best First Search, Grey Wolf Optimizer (GWO)
"""

import sys
import os

# Thêm thư mục gốc vào Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Core.job import Job
from Core.machine import Machine
from Core.schedule import Schedule
from algorithms.greedy import GreedyScheduler
from algorithms.gwo import GWOScheduler
from utils.data_generator import DataGenerator
from utils.metrics import Metrics
import matplotlib.pyplot as plt
import time


class SchedulingSystem:
    """Hệ thống quản lý và thực thi các thuật toán xếp lịch"""
    
    def __init__(self):
        self.jobs = []
        self.machines = []
        self.results = {}
        
    def setup(self, n_jobs=10, n_machines=3, duration_range=(1, 20), deadline_range=(5, 50)):
        """Khởi tạo dữ liệu jobs và machines"""
        self.jobs = DataGenerator.generate_jobs(
            n_jobs, 
            duration_range=duration_range,
            deadline_range=deadline_range
        )
        self.machines = [Machine(i) for i in range(n_machines)]
        print(f"✅ Đã tạo {n_jobs} jobs và {n_machines} machines")
        
    def run_greedy(self, strategy="SPT"):
        """Chạy thuật toán Greedy"""
        print(f"\n🔄 Đang chạy Greedy ({strategy})...")
        start_time = time.time()
        
        scheduler = GreedyScheduler(self.jobs, self.machines, strategy=strategy)
        schedule = scheduler.schedule()
        
        runtime = time.time() - start_time
        metrics = schedule.evaluate()
        
        self.results[f"Greedy_{strategy}"] = {
            "schedule": schedule,
            "makespan": metrics["makespan"],
            "total_lateness": metrics["total_lateness"],
            "runtime": runtime
        }
        
        print(f"✅ Greedy ({strategy}): Makespan = {metrics['makespan']:.2f}, Runtime = {runtime:.4f}s")
        return schedule
        
    def run_gwo(self, pop_size=30, iters=100):
        """Chạy thuật toán Grey Wolf Optimizer"""
        print(f"\n🔄 Đang chạy GWO (pop={pop_size}, iters={iters})...")
        start_time = time.time()
        
        # Chuyển jobs thành format cho GWO
        job_durations = [job.duration for job in self.jobs]
        
        from algorithms.gwo import gwo_schedule
        schedule_result, makespan, info = gwo_schedule(
            jobs=job_durations,
            m=len(self.machines),
            pop_size=pop_size,
            iters=iters,
            verbose=False
        )
        
        runtime = time.time() - start_time
        
        self.results["GWO"] = {
            "schedule": schedule_result,
            "makespan": makespan,
            "runtime": runtime,
            "info": info
        }
        
        print(f"✅ GWO: Makespan = {makespan:.2f}, Runtime = {runtime:.4f}s")
        return schedule_result
        
    def compare_algorithms(self):
        """So sánh kết quả các thuật toán"""
        print("\n" + "="*60)
        print("📊 SO SÁNH KẾT QUẢ CÁC THUẬT TOÁN")
        print("="*60)
        
        for name, result in self.results.items():
            print(f"\n{name}:")
            print(f"  - Makespan: {result['makespan']:.2f}")
            if 'total_lateness' in result:
                print(f"  - Total Lateness: {result['total_lateness']:.2f}")
            print(f"  - Runtime: {result['runtime']:.4f}s")
            
    def visualize_comparison(self):
        """Vẽ biểu đồ so sánh"""
        if not self.results:
            print("⚠️ Chưa có kết quả để so sánh!")
            return
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Biểu đồ Makespan
        names = list(self.results.keys())
        makespans = [self.results[k]["makespan"] for k in names]
        
        ax1.bar(names, makespans, color=['#3498db', '#e74c3c', '#2ecc71'][:len(names)])
        ax1.set_ylabel('Makespan (time units)')
        ax1.set_title('So sánh Makespan')
        ax1.grid(axis='y', alpha=0.3)
        
        # Biểu đồ Runtime
        runtimes = [self.results[k]["runtime"] for k in names]
        
        ax2.bar(names, runtimes, color=['#9b59b6', '#f39c12', '#1abc9c'][:len(names)])
        ax2.set_ylabel('Runtime (seconds)')
        ax2.set_title('So sánh Thời gian chạy')
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
    def print_schedule_details(self, algo_name):
        """In chi tiết lịch phân công"""
        if algo_name not in self.results:
            print(f"⚠️ Không tìm thấy kết quả cho {algo_name}")
            return
            
        print(f"\n📋 CHI TIẾT LỊCH - {algo_name}")
        print("="*60)
        
        result = self.results[algo_name]
        
        if "schedule" in result and isinstance(result["schedule"], Schedule):
            schedule = result["schedule"]
            for machine in schedule.machines:
                print(f"\nMachine {machine.machine_id}:")
                for job, start, finish in machine.schedule:
                    print(f"  Job {job.job_id}: [{start:.1f} - {finish:.1f}] (duration: {job.duration})")


def demo_basic():
    """Demo cơ bản - chạy tất cả thuật toán"""
    print("="*60)
    print("🚀 DEMO HỆ THỐNG XẾP LỊCH CÔNG VIỆC")
    print("="*60)
    
    system = SchedulingSystem()
    system.setup(n_jobs=15, n_machines=4)
    
    # Chạy các thuật toán
    system.run_greedy(strategy="SPT")
    system.run_greedy(strategy="EDD")
    system.run_gwo(pop_size=30, iters=100)
    
    # So sánh kết quả
    system.compare_algorithms()
    
    # In chi tiết lịch
    system.print_schedule_details("Greedy_SPT")
    
    # Vẽ biểu đồ
    system.visualize_comparison()


def demo_scale_test():
    """Demo test với quy mô khác nhau"""
    print("="*60)
    print("📈 TEST HIỆU NĂNG VỚI QUY MÔ KHÁC NHAU")
    print("="*60)
    
    scales = [(10, 3), (20, 5), (30, 6), (50, 8)]
    
    results_spt = []
    results_gwo = []
    
    for n_jobs, n_machines in scales:
        print(f"\n--- Test với {n_jobs} jobs, {n_machines} machines ---")
        
        system = SchedulingSystem()
        system.setup(n_jobs=n_jobs, n_machines=n_machines)
        
        system.run_greedy(strategy="SPT")
        system.run_gwo(pop_size=20, iters=50)
        
        results_spt.append(system.results["Greedy_SPT"]["makespan"])
        results_gwo.append(system.results["GWO"]["makespan"])
    
    # Vẽ biểu đồ so sánh scaling
    plt.figure(figsize=(10, 6))
    x_labels = [f"{j}j/{m}m" for j, m in scales]
    x = range(len(x_labels))
    
    plt.plot(x, results_spt, marker='o', label='Greedy SPT', linewidth=2)
    plt.plot(x, results_gwo, marker='s', label='GWO', linewidth=2)
    
    plt.xlabel('Problem Size (jobs/machines)')
    plt.ylabel('Makespan')
    plt.title('Hiệu năng thuật toán theo quy mô bài toán')
    plt.xticks(x, x_labels)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("   CHƯƠNG TRÌNH XẾP LỊCH CÔNG VIỆC - ĐỒ ÁN AI")
    print("   Nhóm 8 - Greedy & Grey Wolf Optimizer")
    print("="*60)
    
    while True:
        print("\n📋 MENU:")
        print("1. Demo cơ bản")
        print("2. Test hiệu năng theo quy mô")
        print("3. Chạy GUI (Tkinter)")
        print("4. Thoát")
        
        choice = input("\n👉 Chọn chức năng (1-4): ").strip()
        
        if choice == "1":
            demo_basic()
        elif choice == "2":
            demo_scale_test()
        elif choice == "3":
            print("\n🖥️ Đang khởi động GUI...")
            from GUI import SchedulingGUI
            SchedulingGUI().run()
        elif choice == "4":
            print("\n👋 Cảm ơn đã sử dụng chương trình!")
            break
        else:
            print("⚠️ Lựa chọn không hợp lệ!")