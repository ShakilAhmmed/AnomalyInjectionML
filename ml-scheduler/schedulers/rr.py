import json
import pandas as pd

def rr_schedule(data, quantum=10):
    df = pd.DataFrame(data).sort_values('arrival_time')
    time, schedule, ready = 0, [], []
    queue = df.to_dict('records')
    remaining = {p['pid']: p['burst_time'] for p in queue}
    idx = 0

    while idx < len(queue) or ready:
        while idx < len(queue) and queue[idx]['arrival_time'] <= time:
            ready.append(queue[idx])
            idx += 1

        if not ready:
            if idx < len(queue):
                time = queue[idx]['arrival_time']
            else:
                break
            continue

        p = ready.pop(0)
        exec_time = min(quantum, remaining[p['pid']])
        schedule.append((time, p['pid']))
        time += exec_time
        remaining[p['pid']] -= exec_time
        if remaining[p['pid']] > 0:
            ready.append(p)

    return schedule

if __name__ == '__main__':
    with open("dataset/testing/uniform_test.json") as f:
        data = json.load(f)
    print("RR:", rr_schedule(data))