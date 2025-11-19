"""
GUI APPLICATION - HỆ THỐNG XẾP LỊCH CÔNG VIỆC
Sử dụng Tkinter + Matplotlib
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Core.job import Job
from Core.machine import Machine
from algorithms.greedy import GreedyScheduler
from algorithms.gwo import gwo_schedule
from utils.data_generator import DataGenerator
import time


class SchedulingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hệ Thống Xếp Lịch Công Việc - Đồ Án AI")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
        
        # Data
        self.jobs = []
        self.machines = []
        self.results = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # === LEFT PANEL - Control ===
        self.setup_control_panel(main_frame)
        
        # === RIGHT PANEL - Visualization ===
        self.setup_visualization_panel(main_frame)
        
        # === BOTTOM PANEL - Results ===
        self.setup_results_panel(main_frame)
        
    def setup_control_panel(self, parent):
        """Panel điều khiển bên trái"""
        control_frame = ttk.LabelFrame(parent, text="⚙️ Cấu Hình & Điều Khiển", padding="10")
        control_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # === Input Parameters ===
        params_frame = ttk.LabelFrame(control_frame, text="Tham Số Đầu Vào", padding="10")
        params_frame.pack(fill=tk.X, pady=5)
        
        # Number of jobs
        ttk.Label(params_frame, text="Số lượng Jobs:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.n_jobs_var = tk.IntVar(value=15)
        ttk.Entry(params_frame, textvariable=self.n_jobs_var, width=10).grid(row=0, column=1, pady=5)
        
        # Number of machines
        ttk.Label(params_frame, text="Số lượng Machines:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.n_machines_var = tk.IntVar(value=4)
        ttk.Entry(params_frame, textvariable=self.n_machines_var, width=10).grid(row=1, column=1, pady=5)
        
        # Duration range
        ttk.Label(params_frame, text="Duration Range:").grid(row=2, column=0, sticky=tk.W, pady=5)
        dur_frame = ttk.Frame(params_frame)
        dur_frame.grid(row=2, column=1, pady=5)
        self.dur_min_var = tk.IntVar(value=1)
        self.dur_max_var = tk.IntVar(value=20)
        ttk.Entry(dur_frame, textvariable=self.dur_min_var, width=5).pack(side=tk.LEFT)
        ttk.Label(dur_frame, text="-").pack(side=tk.LEFT, padx=2)
        ttk.Entry(dur_frame, textvariable=self.dur_max_var, width=5).pack(side=tk.LEFT)
        
        # Deadline range
        ttk.Label(params_frame, text="Deadline Range:").grid(row=3, column=0, sticky=tk.W, pady=5)
        dead_frame = ttk.Frame(params_frame)
        dead_frame.grid(row=3, column=1, pady=5)
        self.dead_min_var = tk.IntVar(value=5)
        self.dead_max_var = tk.IntVar(value=50)
        ttk.Entry(dead_frame, textvariable=self.dead_min_var, width=5).pack(side=tk.LEFT)
        ttk.Label(dead_frame, text="-").pack(side=tk.LEFT, padx=2)
        ttk.Entry(dead_frame, textvariable=self.dead_max_var, width=5).pack(side=tk.LEFT)
        
        # Generate button
        ttk.Button(params_frame, text="🔄 Tạo Dữ Liệu", command=self.generate_data).grid(
            row=4, column=0, columnspan=2, pady=10, sticky=tk.EW
        )
        
        # === Algorithm Selection ===
        algo_frame = ttk.LabelFrame(control_frame, text="Chọn Thuật Toán", padding="10")
        algo_frame.pack(fill=tk.X, pady=5)
        
        # Greedy options
        greedy_frame = ttk.LabelFrame(algo_frame, text="Greedy Algorithm", padding="5")
        greedy_frame.pack(fill=tk.X, pady=5)
        
        self.greedy_strategy_var = tk.StringVar(value="SPT")
        ttk.Radiobutton(greedy_frame, text="SPT (Shortest Processing Time)", 
                       variable=self.greedy_strategy_var, value="SPT").pack(anchor=tk.W)
        ttk.Radiobutton(greedy_frame, text="EDD (Earliest Due Date)", 
                       variable=self.greedy_strategy_var, value="EDD").pack(anchor=tk.W)
        ttk.Radiobutton(greedy_frame, text="FCFS (First Come First Served)", 
                       variable=self.greedy_strategy_var, value="FCFS").pack(anchor=tk.W)
        
        ttk.Button(greedy_frame, text="▶️ Chạy Greedy", command=self.run_greedy).pack(
            fill=tk.X, pady=5
        )
        
        # GWO options
        gwo_frame = ttk.LabelFrame(algo_frame, text="Grey Wolf Optimizer", padding="5")
        gwo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(gwo_frame, text="Population Size:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.gwo_pop_var = tk.IntVar(value=30)
        ttk.Entry(gwo_frame, textvariable=self.gwo_pop_var, width=10).grid(row=0, column=1, pady=2)
        
        ttk.Label(gwo_frame, text="Iterations:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.gwo_iter_var = tk.IntVar(value=100)
        ttk.Entry(gwo_frame, textvariable=self.gwo_iter_var, width=10).grid(row=1, column=1, pady=2)
        
        ttk.Button(gwo_frame, text="▶️ Chạy GWO", command=self.run_gwo).grid(
        row=2, column=0, columnspan=2, sticky=tk.EW, pady=5
    )
        
        # === Action Buttons ===
        action_frame = ttk.Frame(control_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="🏃 Chạy Tất Cả", 
                  command=self.run_all_algorithms).pack(fill=tk.X, pady=2)
        ttk.Button(action_frame, text="📊 So Sánh", 
                  command=self.show_comparison).pack(fill=tk.X, pady=2)
        ttk.Button(action_frame, text="🗑️ Xóa Kết Quả", 
                  command=self.clear_results).pack(fill=tk.X, pady=2)
        
        # Status
        self.status_label = ttk.Label(control_frame, text="Trạng thái: Chờ dữ liệu...", 
                                     foreground="blue")
        self.status_label.pack(pady=10)
        
    def setup_visualization_panel(self, parent):
        """Panel hiển thị biểu đồ"""
        viz_frame = ttk.LabelFrame(parent, text="📈 Trực Quan Hóa", padding="10")
        viz_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(8, 6), dpi=80)
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initial plot
        ax = self.fig.add_subplot(111)
        ax.text(0.5, 0.5, 'Chưa có dữ liệu để hiển thị', 
               ha='center', va='center', fontsize=16)
        ax.axis('off')
        self.canvas.draw()
        
    def setup_results_panel(self, parent):
        """Panel hiển thị kết quả"""
        results_frame = ttk.LabelFrame(parent, text="📋 Kết Quả Chi Tiết", padding="10")
        results_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Scrolled text for results - BỎ width cố định để có thể resize
        self.results_text = scrolledtext.ScrolledText(results_frame, 
                                                    font=("Courier", 10),
                                                    wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Insert initial text
        self.results_text.insert(tk.END, "Chờ kết quả từ thuật toán...\n")
        self.results_text.config(state=tk.DISABLED)
        
    def generate_data(self):
        """Tạo dữ liệu jobs và machines"""
        try:
            n_jobs = self.n_jobs_var.get()
            n_machines = self.n_machines_var.get()
            dur_range = (self.dur_min_var.get(), self.dur_max_var.get())
            dead_range = (self.dead_min_var.get(), self.dead_max_var.get())
            
            if n_jobs <= 0 or n_machines <= 0:
                raise ValueError("Số lượng phải > 0")
            
            self.jobs = DataGenerator.generate_jobs(n_jobs, dur_range, dead_range)
            self.machines = [Machine(i) for i in range(n_machines)]
            self.results = {}
            
            self.status_label.config(text=f"✅ Đã tạo {n_jobs} jobs, {n_machines} machines", 
                                    foreground="green")
            
            # Show job data
            self.show_job_data()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo dữ liệu: {str(e)}")
            
    def show_job_data(self):
        """Hiển thị thông tin jobs"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, "="*80 + "\n")
        self.results_text.insert(tk.END, "DANH SÁCH JOBS\n")
        self.results_text.insert(tk.END, "="*80 + "\n")
        self.results_text.insert(tk.END, f"{'ID':<5} {'Duration':<10} {'Deadline':<10} {'Priority':<10}\n")
        self.results_text.insert(tk.END, "-"*80 + "\n")
        
        for job in self.jobs:
            self.results_text.insert(tk.END, 
                f"{job.job_id:<5} {job.duration:<10} {job.deadline:<10} {job.priority:<10}\n")
        
        self.results_text.config(state=tk.DISABLED)
        
        # Visualize jobs
        self.visualize_jobs()
        
    def visualize_jobs(self):
        """Vẽ biểu đồ phân bố jobs"""
        self.fig.clear()
        
        ax1 = self.fig.add_subplot(121)
        durations = [job.duration for job in self.jobs]
        ax1.hist(durations, bins=10, color='skyblue', edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Duration')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Phân Bố Thời Gian Jobs')
        ax1.grid(alpha=0.3)
        
        ax2 = self.fig.add_subplot(122)
        deadlines = [job.deadline for job in self.jobs]
        ax2.hist(deadlines, bins=10, color='lightcoral', edgecolor='black', alpha=0.7)
        ax2.set_xlabel('Deadline')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Phân Bố Deadline')
        ax2.grid(alpha=0.3)
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def run_greedy(self):
        """Chạy thuật toán Greedy"""
        if not self.jobs:
            messagebox.showwarning("Cảnh báo", "Vui lòng tạo dữ liệu trước!")
            return
        
        try:
            strategy = self.greedy_strategy_var.get()
            self.status_label.config(text=f"⏳ Đang chạy Greedy ({strategy})...", 
                                    foreground="orange")
            self.root.update()
            
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
            
            self.status_label.config(
                text=f"✅ Greedy ({strategy}): Makespan={metrics['makespan']:.2f}, Time={runtime:.4f}s", 
                foreground="green"
            )
            
            self.display_results(f"Greedy_{strategy}")
            self.visualize_gantt_chart(schedule, f"Greedy {strategy}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi chạy Greedy: {str(e)}")
            self.status_label.config(text="❌ Lỗi khi chạy Greedy", foreground="red")
            
    def run_gwo(self):
        """Chạy thuật toán GWO"""
        if not self.jobs:
            messagebox.showwarning("Cảnh báo", "Vui lòng tạo dữ liệu trước!")
            return
        
        try:
            pop_size = self.gwo_pop_var.get()
            iters = self.gwo_iter_var.get()
            
            self.status_label.config(text=f"⏳ Đang chạy GWO...", foreground="orange")
            self.root.update()
            
            job_durations = [job.duration for job in self.jobs]
            
            start_time = time.time()
            schedule, makespan, info = gwo_schedule(
                jobs=job_durations,
                m=len(self.machines),
                pop_size=pop_size,
                iters=iters,
                verbose=False
            )
            runtime = time.time() - start_time
            
            self.results["GWO"] = {
                "schedule": schedule,
                "makespan": makespan,
                "runtime": runtime,
                "info": info
            }
            
            self.status_label.config(
                text=f"✅ GWO: Makespan={makespan:.2f}, Time={runtime:.4f}s", 
                foreground="green"
            )
            
            self.display_results("GWO")
            self.visualize_gwo_convergence(info)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi chạy GWO: {str(e)}")
            self.status_label.config(text="❌ Lỗi khi chạy GWO", foreground="red")
            
    def run_all_algorithms(self):
        """Chạy tất cả thuật toán"""
        self.run_greedy()
        self.run_gwo()
        self.show_comparison()
        
    def display_results(self, algo_name):
        """Hiển thị kết quả chi tiết"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        result = self.results[algo_name]
        
        self.results_text.insert(tk.END, "="*80 + "\n")
        self.results_text.insert(tk.END, f"KẾT QUẢ: {algo_name}\n")
        self.results_text.insert(tk.END, "="*80 + "\n\n")
        
        self.results_text.insert(tk.END, f"📊 Makespan: {result['makespan']:.2f}\n")
        self.results_text.insert(tk.END, f"⏱️ Runtime: {result['runtime']:.4f}s\n")
        
        if 'total_lateness' in result:
            self.results_text.insert(tk.END, f"⏰ Total Lateness: {result['total_lateness']:.2f}\n")
        
        self.results_text.insert(tk.END, "\n" + "-"*80 + "\n")
        self.results_text.insert(tk.END, "LỊCH PHÂN CÔNG:\n")
        self.results_text.insert(tk.END, "-"*80 + "\n\n")
        
        if "schedule" in result and hasattr(result["schedule"], "machines"):
            schedule = result["schedule"]
            for machine in schedule.machines:
                self.results_text.insert(tk.END, f"\nMachine {machine.machine_id}:\n")
                for job, start, finish in machine.schedule:
                    self.results_text.insert(tk.END, 
                        f"  Job {job.job_id}: [{start:.1f} - {finish:.1f}] (dur: {job.duration})\n")
        elif "schedule" in result:
            # GWO format
            schedule = result["schedule"]
            for m_idx, jobs_on_machine in enumerate(schedule):
                self.results_text.insert(tk.END, f"\nMachine {m_idx}:\n")
                self.results_text.insert(tk.END, f"  Jobs: {jobs_on_machine}\n")
        
        self.results_text.config(state=tk.DISABLED)
        
    def visualize_gantt_chart(self, schedule, title):
        """Vẽ biểu đồ Gantt"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        colors = plt.cm.Set3(range(len(schedule.machines)))
        
        for idx, machine in enumerate(schedule.machines):
            for job, start, finish in machine.schedule:
                ax.barh(idx, finish - start, left=start, height=0.8, 
                       color=colors[idx], edgecolor='black', alpha=0.8)
                ax.text(start + (finish - start)/2, idx, f"J{job.job_id}", 
                       ha='center', va='center', fontsize=8, weight='bold')
        
        ax.set_xlabel('Time', fontsize=10)
        ax.set_ylabel('Machine', fontsize=10)
        ax.set_title(f'Gantt Chart - {title}', fontsize=12, weight='bold')
        ax.set_yticks(range(len(schedule.machines)))
        ax.set_yticklabels([f"M{m.machine_id}" for m in schedule.machines])
        ax.grid(axis='x', alpha=0.3)
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def visualize_gwo_convergence(self, info):
        """Vẽ đồ thị hội tụ GWO"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        history = info["best_history"]
        ax.plot(history, linewidth=2, color='#e74c3c')
        ax.set_xlabel('Iteration', fontsize=10)
        ax.set_ylabel('Best Makespan', fontsize=10)
        ax.set_title('GWO Convergence Curve', fontsize=12, weight='bold')
        ax.grid(alpha=0.3)
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def show_comparison(self):
        """Hiển thị so sánh các thuật toán"""
        if len(self.results) < 2:
            messagebox.showinfo("Thông báo", "Cần chạy ít nhất 2 thuật toán để so sánh!")
            return
        
        self.fig.clear()
        
        names = list(self.results.keys())
        makespans = [self.results[k]["makespan"] for k in names]
        runtimes = [self.results[k]["runtime"] for k in names]
        
        # Makespan comparison
        ax1 = self.fig.add_subplot(121)
        bars1 = ax1.bar(names, makespans, color=['#3498db', '#e74c3c', '#2ecc71'][:len(names)])
        ax1.set_ylabel('Makespan', fontsize=10)
        ax1.set_title('So Sánh Makespan', fontsize=11, weight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=9)
        
        # Runtime comparison
        ax2 = self.fig.add_subplot(122)
        bars2 = ax2.bar(names, runtimes, color=['#9b59b6', '#f39c12', '#1abc9c'][:len(names)])
        ax2.set_ylabel('Runtime (s)', fontsize=10)
        ax2.set_title('So Sánh Thời Gian', fontsize=11, weight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}', ha='center', va='bottom', fontsize=9)
        
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Display comparison in text
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, "="*80 + "\n")
        self.results_text.insert(tk.END, "SO SÁNH CÁC THUẬT TOÁN\n")
        self.results_text.insert(tk.END, "="*80 + "\n\n")
        
        for name, result in self.results.items():
            self.results_text.insert(tk.END, f"🔹 {name}:\n")
            self.results_text.insert(tk.END, f"   Makespan: {result['makespan']:.2f}\n")
            self.results_text.insert(tk.END, f"   Runtime: {result['runtime']:.4f}s\n")
            if 'total_lateness' in result:
                self.results_text.insert(tk.END, f"   Total Lateness: {result['total_lateness']:.2f}\n")
            self.results_text.insert(tk.END, "\n")
        
        self.results_text.config(state=tk.DISABLED)
        
    def clear_results(self):
        """Xóa kết quả"""
        self.results = {}
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Đã xóa kết quả.\n")
        self.results_text.config(state=tk.DISABLED)
        
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.text(0.5, 0.5, 'Chưa có dữ liệu để hiển thị', 
               ha='center', va='center', fontsize=14)
        ax.axis('off')
        self.canvas.draw()
        
        self.status_label.config(text="🗑️ Đã xóa kết quả", foreground="blue")
        
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()


if __name__ == "__main__":
    app = SchedulingGUI()
    app.run()