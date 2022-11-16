import os
import pandas as pd
import numpy as np
import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--output_path", type=str)

    return parser.parse_args()


def run(output_path):
    job_statistics = pd.read_csv(os.path.join(output_path, "job-statistics.csv"))
    job_statistics_confidential = job_statistics[
        job_statistics["attach_money"] == "industry."
    ]

    job_statistics = job_statistics[job_statistics["attach_money"] != "industry."]
    job_statistics["business"] = (
        job_statistics["business"].replace({",": ""}, regex=True).astype(int)
    )
    job_statistics["supervisor_account"] = (
        job_statistics["supervisor_account"].replace({",": ""}, regex=True).astype(int)
    )
    job_statistics["attach_money"] = (
        job_statistics["attach_money"]
        .replace({"\$": "", "bn": "000", "m": ""}, regex=True)
        .astype(int)
    )

    job_statistics.to_csv(os.path.join(output_path, "job-statistics-main.csv.csv"))
    job_statistics_confidential.to_csv(
        os.path.join(output_path, "job-statistics-confidentials.csv")
    )


def main(conf):
    output_path = conf.get("output_path")
    run(output_path)


if __name__ == "__main__":
    opts = parse_args()
    conf = vars(opts)

    main(conf)

# PYTHONPATH=./code python3 ./code/preprocess_data.py --output_path ./results/
