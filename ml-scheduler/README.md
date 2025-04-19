## ML-Based CPU Scheduler

Build and evaluate a Machine Learning (ML)-based CPU scheduling algorithm and compare it with traditional scheduling
algorithms such as FIFO, Round Robin (RR), Multilevel Queue (MLQ), and Completely Fair Scheduler (CFS)

- This project implements a CPU scheduler using a machine learning model (Random Forest) and compares it with
  traditional scheduling algorithms like:
- First In First Out (FIFO)
- Round Robin (RR)
- Multilevel Queue (MLQ)
- Completely Fair Scheduler (CFS)

### Structure with Details

- dataset/make_dataset.py [generates synthetic datasets using multiple distributions)]
- training/train_rf_scheduler.py [trains Random Forest using FIFO-based labels]
- schedulers/ml_scheduler.py [schedules using the trained Random Forest model]
- schedulers/fifo.py [FIFO scheduler based on arrival_time order]
- schedulers/rr.py [ Round Robin scheduler using a default quantum of 10]
- schedulers/mlq.py [MLQ splits based on priority and handles in priority order]
- schedulers/cfs.py [ CFS computes virtual runtimes and runs the process with least vruntime]
- results/results_report.ipynb

### Dataset

Generated synthetic datasets using 4 distributions:

1. Uniform
2. Normal
3. Chi-Squared
4. Fisher

Each dataset contains:

1. pid: Process ID
2. arrival_time
3. burst_time
4. priority

Python scripts used:

1. dataset/make_dataset.py: Core generator
2. dataset/make_testing_data.py
3. dataset/make_training_data.py

Model Training (Random Forest):

1. Model: RandomForestClassifier
2. Features: arrival_time, burst_time, priority
3. Label: Binary class based on median burst_time (short vs long job)

Script: training/train_rf_scheduler.py

Training Steps:

1. Load training data
2. Create binary labels: short job (1) / long job (0)
3. Train RF model
4. Save model to schedulers/rf_model.pkl

Implemented Schedulers:
Each scheduler takes a list of processes (from JSON file) and outputs a list of scheduled (time, PID).

1. FIFO Scheduler
    * Sorts by arrival time and runs in order
    * Script: schedulers/fifo.py
2. Round Robin (RR)
    * Fixed quantum time-slicing (10)
    * Optimized with jump-ahead idle handling
    * Script: schedulers/rr.py
3. Multilevel Queue (MLQ)
    * Splits into two priority queues (0-2 and 3-5)
    * High priority runs first
    * Script: schedulers/mlq.py

4. Completely Fair Scheduler (CFS)
    * Uses virtual runtime concept
    * Lower vruntime process is selected
    * Script: schedulers/cfs.py
5. ML Scheduler
    * Uses trained model to predict next process
    * Fallback to FIFO when model prediction fails
    * Class-based env-style architecture
    * Script: schedulers/ml_scheduler.py

Evaluation Metrics:

* Script: results/evaluation_metrics.py
* For each scheduler:
    * Average Waiting Time
    * Average Turnaround Time
    * CPU Utilization

Results Visualization:

* Script: results_report.ipynb
* Loads testing JSON
* Runs all 5 schedulers
* Calculates metrics
* Plots bar chart
* Saved to: results/evaluation_metrics.csv

## How to Run the Project (Step-by-Step)

### 1. Generate Datasets

```bash
python3 dataset/make_training_data.py
python3 dataset/make_testing_data.py
```

### 2.Train the ML Model

```bash
python3 training/train_rf_scheduler.py
```

This will generate schedulers/rf_model.pkl — the trained RandomForestClassifier.

### 3. Run Individual Schedulers

```bash
python3 schedulers/fifo.py   
python3 schedulers/rr.py    
python3 schedulers/mlq.py 
python3 schedulers/cfs.py 
python3 schedulers/ml_scheduler.py 
```

### Compare and Evaluate All Schedulers

```bash
run results_report.ipynb
```

### Why We Chose RandomForestClassifier

In our CPU scheduling context, the goal is to predict which process should be scheduled earlier, based on features like
arrival time, burst time, and priority.
We chose RandomForestClassifier because it fits this structured decision-making scenario very well:

* Random Forest considers combinations of arrival, burst, and priority to learn scheduling behavior.
* Some short jobs may have high priority, others may not. RF captures these variations
* Since the training dataset is small and synthetically generated, RF prevents overfitting better than single decision
  trees
* We can later extract feature importance to understand which process attributes influence scheduling the most
* Works well with our small training set and integrates smoothly with pandas/sklearn pipeline.

### How it works in our context:

* Features: [arrival_time, burst_time, priority]
* Label: 1 if the process is a short job (burst_time < median), else 0
* Training:
    * The model learns which features indicate short jobs.
* Prediction
    * During scheduling, we use the trained model to predict whether a process is a short job.
    * The scheduler picks the predicted short job to run earlier.
  
### Why ML Performed Better

Traditional schedulers like FIFO and RR follow fixed rules and can't adapt to the nature of the processes. ML-based
scheduling learns patterns from process features like burst time, priority, and arrival time.

* ML learned to prioritize shorter and urgent jobs automatically.
* Used fallback logic to avoid failure
* Maintained high CPU utilization while reducing wait and turnaround time.
* ML scheduler showed lowest waiting and turnaround time in the test dataset
* CPU utilization was close to 100% for all schedulers
* CFS and ML outperformed RR and FIFO in efficiency






