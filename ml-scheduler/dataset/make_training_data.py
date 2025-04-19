import os

distributions = ["normal", "uniform", "chi-squared", "fisher"]

for dist in distributions:
    print(f"Generating training data for {dist} distribution...")
    os.system(f"python dataset/make_dataset.py --distribution {dist} --type train --outdir dataset")
