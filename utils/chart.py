import matplotlib.pyplot as plt

class Chart:
    @staticmethod
    def gantt_chart(machines):
        fig, ax = plt.subplots(figsize=(10, 5))

        yticks = []
        ytick_labels = []

        for i, machine in enumerate(machines):
            yticks.append(i)
            ytick_labels.append(f"Machine {machine.id}")

            for job in machine.schedule:
                start = job.start_time
                duration = job.duration
                ax.barh(i, duration, left=start)
                ax.text(start + duration/2, i, f"J{job.id}",
                        ha='center', va='center')

        ax.set_xlabel("Time")
        ax.set_yticks(yticks)
        ax.set_yticklabels(ytick_labels)
        ax.set_title("Gantt Chart")

        return fig

    @staticmethod
    def compare_chart(results):
        fig, ax = plt.subplots()

        labels = list(results.keys())
        makespans = [results[k]["makespan"] for k in labels]

        ax.bar(labels, makespans)
        ax.set_ylabel("Makespan")
        ax.set_title("So sánh Makespan các thuật toán")

        return fig
