import json
import pandas as pd


def cfs_schedule(data):
    df = pd.DataFrame(data)
    df['vruntime'] = 0
    df = df.sort_values('arrival_time')
    time, schedule, active, idx = 0, [], [], 0

    while len(schedule) < len(df):
        while idx < len(df) and df.iloc[idx]['arrival_time'] <= time:
            active.append(df.iloc[idx].to_dict())
            idx += 1

        if not active:
            time += 1
            continue

        active.sort(key=lambda x: x['vruntime'])
        proc = active.pop(0)
        schedule.append((time, proc['pid']))
        time += proc['burst_time']

        for p in active:
            p['vruntime'] += p['burst_time'] / p['priority']

    return schedule


if __name__ == '__main__':
    with open("dataset/testing/uniform_test.json") as f:
        data = json.load(f)
    print("CFS:", cfs_schedule(data))
