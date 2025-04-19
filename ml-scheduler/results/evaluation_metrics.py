import pandas as pd


def calculate_metrics(schedule, original_data):
    df = pd.DataFrame(original_data).set_index('pid')
    completion_times = {}
    waiting_times = []
    turnaround_times = []

    for time, pid in schedule:
        proc = df.loc[pid]
        start_time = max(time, proc['arrival_time'])
        finish_time = start_time + proc['burst_time']
        waiting_time = start_time - proc['arrival_time']
        turnaround_time = finish_time - proc['arrival_time']
        completion_times[pid] = finish_time
        waiting_times.append(waiting_time)
        turnaround_times.append(turnaround_time)

    avg_waiting = sum(waiting_times) / len(waiting_times)
    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    total_time = max(completion_times.values())
    total_burst = df['burst_time'].sum()
    cpu_util = total_burst / total_time

    return avg_waiting, avg_turnaround, cpu_util
