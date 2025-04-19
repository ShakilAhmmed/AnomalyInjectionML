import json
import pandas as pd

def fifo_schedule(data):
    df = pd.DataFrame(data).sort_values("arrival_time")
    time, schedule = 0, []
    for _, p in df.iterrows():
        if time < p["arrival_time"]:
            time = p["arrival_time"]
        schedule.append((time, int(p["pid"])))
        time += p["burst_time"]
    return schedule

if __name__ == "__main__":
    with open("dataset/testing/uniform_test.json") as f:
        data = json.load(f)
    print("FIFO:", fifo_schedule(data))