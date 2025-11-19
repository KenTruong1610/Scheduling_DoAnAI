import matplotlib.pyplot as plt

class Chart:
    @staticmethod
    def gantt_chart(machines):
        """Vẽ biểu đồ Gantt"""
        fig, ax = plt.subplots(figsize=(10, 5))

        yticks = []
        ytick_labels = []

        for i, machine in enumerate(machines):
            yticks.append(i)
            ytick_labels.append(f"Machine {machine.machine_id}")  # Fix: machine.id -> machine.machine_id

            for job, start, finish in machine.schedule:
                duration = finish - start
                ax.barh(i, duration, left=start, alpha=0.8, edgecolor='black')
                ax.text(start + duration/2, i, f"J{job.job_id}",
                        ha='center', va='center', fontsize=9, weight='bold')

        ax.set_xlabel("Time")
        ax.set_yticks(yticks)
        ax.set_yticklabels(ytick_labels)
        ax.set_title("Gantt Chart")
        ax.grid(axis='x', alpha=0.3)

        return fig

    @staticmethod
    def compare_chart(results):
        """So sánh makespan các thuật toán"""
        fig, ax = plt.subplots()

        labels = list(results.keys())
        makespans = [results[k]["makespan"] for k in labels]

        bars = ax.bar(labels, makespans, color=['#3498db', '#e74c3c', '#2ecc71'])
        ax.set_ylabel("Makespan")
        ax.set_title("So sánh Makespan các thuật toán")
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom')

        return fig