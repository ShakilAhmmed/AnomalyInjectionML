import json
import pandas as pd


def mlq_schedule(data):
    df = pd.DataFrame(data)
    df['queue_level'] = df['priority'].apply(lambda x: 0 if x <= 2 else 1)
    q0 = df[df['queue_level'] == 0].sort_values('arrival_time')
    q1 = df[df['queue_level'] == 1].sort_values('arrival_time')

    time, schedule, i0, i1 = 0, [], 0, 0
    q0, q1 = q0.to_dict('records'), q1.to_dict('records')

    while i0 < len(q0) or i1 < len(q1):
        ready0 = [p for p in q0[i0:] if p['arrival_time'] <= time]
        ready1 = [p for p in q1[i1:] if p['arrival_time'] <= time]

        if ready0:
            p = ready0[0]
            schedule.append((time, p['pid']))
            time += p['burst_time']
            i0 += 1
        elif ready1:
            p = ready1[0]
            schedule.append((time, p['pid']))
            time += p['burst_time']
            i1 += 1
        else:
            time += 1

    return schedule


if __name__ == '__main__':
    with open("dataset/testing/uniform_test.json") as f:
        data = json.load(f)
    print("MLQ:", mlq_schedule(data))
