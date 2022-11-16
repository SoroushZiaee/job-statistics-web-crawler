# Web Scrapping Packages
from selenium import webdriver
from bs4 import BeautifulSoup

# General Packages
import numpy as np
import re
from tqdm import tqdm
import pandas as pd
import os


def get_driver(driver_path: str = "./chromedriver"):
    print(" - Connect to Chrome")

    options = webdriver.ChromeOptions()

    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")

    # Prevent from openning the browser
    options.add_argument("--headless")
    driver = webdriver.Chrome(driver_path, chrome_options=options)

    return driver


def get_url(driver, url: str):
    driver.get(url)


def get_page_source(driver):
    return driver.page_source


def get_soup(page_source):
    return BeautifulSoup(page_source, "lxml")


def retrieve_list_link(soup):
    return [
        link.get("href")
        for link in tqdm(
            soup.find_all("a", attrs={"href": re.compile("^/au/industry/")}),
            desc="Get links",
        )
    ]


def get_list_link(driver_path: str, url: str):

    print(" - get the links")
    driver = get_driver(driver_path)
    get_url(driver, url)

    page_source = get_page_source(driver)
    soup = get_soup(page_source)

    driver.quit()

    return retrieve_list_link(soup)


def get_job_statistics(driver, url: str):
    get_url(driver, url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    div = soup.find("div", {"id": "KeyStatsTiles"})
    uls = div.findAll("ul")
    lis = np.array([li.text for ul in uls for li in ul.findAll("li")])[[0, 1, 3]]

    output = [li.split()[-1] for li in lis]

    return output


def get_list_statistics(driver_path: str, url_format: str, links, output_path: str):
    print("- Get job statistics")

    driver = get_driver(driver_path)

    statistics = load_statistics(output_path)
    if len(statistics) != 0:
        links = load_links(links, list(map(lambda x: x[0], statistics)))

    for link in tqdm(links, desc="Get the statistics data"):
        try:
            statistics.append(
                [link.split("/")[3]]
                + get_job_statistics(
                    driver,
                    url_format.format(link),
                )
            )
        except Exception as e:
            statistics.append([link.split("/")[3]] + [0, 0, 0])
            print(f"An Expection occured in : {link.split('/')[3]}")
            print(f"the Error is {e}")

        save_df(statistics, output_path)

    return statistics


def load_statistics(output_path: str):
    data_path = os.path.join(output_path, "job-statistics.csv")
    if os.path.exists(data_path):
        return list(pd.read_csv(data_path).to_numpy())

    return []


def load_links(links, links_retrieved):
    links = np.array(links)
    modified_links = np.array([link.split("/")[3] for link in links])
    idx = np.isin(modified_links, links_retrieved)
    return links[~idx]


def save_df(x, output_path):
    df = pd.DataFrame(
        x, columns=["Name", "attach_money", "business", "supervisor_account"]
    )
    df.to_csv(os.path.join(output_path, "job-statistics.csv"), index=False)
