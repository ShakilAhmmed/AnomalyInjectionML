import argparse
import json
import os
import numpy as np


def generate_data(num_processes, distribution):
    if distribution == "normal":
        arrival_times = np.abs(np.random.normal(25, 10, num_processes).astype(int))
        burst_times = np.abs(np.random.normal(10, 3, num_processes).astype(int)) + 1
    elif distribution == "uniform":
        arrival_times = np.random.randint(0, 50, num_processes)
        burst_times = np.random.randint(1, 20, num_processes)
    elif distribution == "chi-squared":
        arrival_times = np.random.chisquare(2, num_processes).astype(int)
        burst_times = np.random.chisquare(5, num_processes).astype(int) + 1
    elif distribution == "fisher":
        arrival_times = np.random.f(2, 5, num_processes).astype(int)
        burst_times = np.random.f(5, 2, num_processes).astype(int) + 1
    else:
        raise ValueError("Invalid distribution")

    data = [{
        "pid": i,
        "arrival_time": int(arrival_times[i]),
        "burst_time": int(burst_times[i]),
        "priority": int(np.random.randint(1, 5))
    } for i in range(num_processes)]

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_processes", type=int, default=100)
    parser.add_argument("--distribution", type=str, default="uniform")
    parser.add_argument("--type", type=str, choices=["train", "test"], default="train")
    parser.add_argument("--outdir", type=str, default="dataset")
    args = parser.parse_args()

    data = generate_data(args.num_processes, args.distribution)
    subdir = "training" if args.type == "train" else "testing"
    os.makedirs(os.path.join(args.outdir, subdir), exist_ok=True)
    filename = f"{args.distribution}_{args.type}.json"
    with open(os.path.join(args.outdir, subdir, filename), "w") as f:
        json.dump(data, f, indent=4)
