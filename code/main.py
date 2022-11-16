import argparse
import os
from pprint import pprint

import pandas as pd

from package import get_list_link, get_list_statistics


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--output_path", type=str)
    parser.add_argument("--get_link", type=bool, default=False)

    return parser.parse_args()


def save_link(output_path: str, links):
    with open(os.path.join(output_path, "links.txt"), "w") as fout:
        for link in links:
            fout.write(f"{link}\n")


def load_link(output_path: str):
    with open(os.path.join(output_path, "links.txt"), "r") as fout:
        lines = fout.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    return lines


def run(output_path: str, is_get_link: bool):
    driver_path = "./chromedriver"
    url = "https://www.ibisworld.com/au/list-of-industries/"

    # Get the links
    if (is_get_link) or (not os.path.exists(os.path.join(output_path, "links.txt"))):
        links = get_list_link(driver_path, url)
        save_link(output_path, links)

    else:
        links = load_link(output_path)

    statistics = get_list_statistics(
        driver_path, "https://www.ibisworld.com/{}", links, output_path
    )

    df = pd.DataFrame(
        statistics, columns=["name", "attach_money", "business", "supervisor_account"]
    )

    df.to_csv(os.path.join(output_path, "job-statistics-2.csv"), index=False)


def main(conf):
    output_path = conf.get("output_path")
    os.makedirs(output_path, exist_ok=True)

    is_get_link = conf.get("get_link")
    run(output_path, is_get_link)


if __name__ == "__main__":
    opts = parse_args()
    conf = vars(opts)

    main(conf)


# Test Script
# PYTHONPATH=./code python3 ./code/main.py --output_path ./results/ --get_link True
