import json
import pandas as pd
import joblib

class MLSchedulerEnv:
    def __init__(self, data_path="dataset/testing/uniform_test.json", model_path="schedulers/rf_model.pkl"):
        print("[INFO] Loading dataset and model...")
        with open(data_path) as f:
            self.data = json.load(f)
        self.df = pd.DataFrame(self.data)
        print(f"[INFO] Total processes loaded: {len(self.df)}")

        self.model = joblib.load(model_path)
        print("[INFO] Model loaded successfully.")
        self.reset()

    def reset(self):
        self.time = 0
        self.schedule = []
        self.df_copy = self.df.copy()
        self.predicted_pids = set()

    def available_processes(self):
        return self.df_copy[self.df_copy['arrival_time'] <= self.time]

    def step(self):
        print(f"[STEP] Current time: {self.time}, remaining: {len(self.df_copy)} processes")
        available = self.available_processes()
        if available.empty:
            if not self.df_copy.empty:
                self.time = self.df_copy['arrival_time'].min()
                print(f"[WAIT] No process ready, time jumped to {self.time}")
            return

        X = available[['arrival_time', 'burst_time', 'priority']]
        preds = self.model.predict(X)

        selected_id = None
        for pid in preds:
            if pid not in self.predicted_pids and pid in available['pid'].values:
                selected_id = pid
                break

        # fallback if model fails
        if selected_id is None and not available.empty:
            fallback_pid = available.iloc[0]['pid']
            print(f"[FALLBACK] No ML decision, falling back to PID {fallback_pid}")
            selected_id = fallback_pid

        process_row = available[available['pid'] == selected_id]
        if process_row.empty:
            self.time += 1
            return

        process = process_row.iloc[0]
        self.schedule.append((self.time, int(process['pid'])))
        self.predicted_pids.add(int(process['pid']))
        print(f"[RUN] Time {self.time}: Running PID {process['pid']} for {process['burst_time']} units")
        self.time += process['burst_time']
        self.df_copy = self.df_copy[self.df_copy['pid'] != selected_id]

    def run(self):
        while not self.df_copy.empty:
            self.step()
        print("[DONE] Scheduling complete.")
        return self.schedule

# Run standalone
if __name__ == "__main__":
    env = MLSchedulerEnv()
    result = env.run()
    print("ML Scheduling Order:", result)