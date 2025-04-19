import os

distributions = ["normal", "uniform", "chi-squared", "fisher"]

for dist in distributions:
    print(f"Generating testing data for {dist} distribution...")
    os.system(f"python dataset/make_dataset.py --distribution {dist} --type test --outdir dataset")
