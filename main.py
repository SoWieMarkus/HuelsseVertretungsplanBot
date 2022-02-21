import subprocess
import requests
import pprint
import os
from datetime import datetime
from bs4 import BeautifulSoup as HTMLParser
from typing import List

from models import Link, Substitution, BASE_URL, TEMP_DIRECTORY, convert_to_json
from pathlib import Path
import csv
import operator
import time

HOME = "/huelsse/home"

SLEEP = 60 * 60


def log(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | "
    if isinstance(message, str):
        print(current_time + message)
    else:
        print(current_time)
        pprint.pprint(message)


def get_links():
    log("Scanning website for links ...")
    result = requests.get(BASE_URL + HOME)
    html = HTMLParser(result.text, "html.parser")
    links = []
    for link_tag in html.find_all("a"):
        href = link_tag["href"]
        if "vertretung" in href:
            link = Link(href, link_tag.text)
            links.append(link)
            log(link.get_url())
    return links


def download_pdf(link: Link):
    file_name = Path(link.get_pdf_path())
    pdf = requests.get(link.get_url())
    file_name.write_bytes(pdf.content)


def create_temp_directory():
    if not os.path.exists(TEMP_DIRECTORY):
        os.mkdir(TEMP_DIRECTORY)


def delete_temp_directory():
    directory = "./" + TEMP_DIRECTORY
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            log('Failed to delete %s. Reason: %s' % (file_path, e))

    if os.path.exists(TEMP_DIRECTORY):
        os.rmdir(TEMP_DIRECTORY)


def convert_to_csv():
    subprocess.call(["java", "-jar", "tabula/tabula.jar", "-p", "all", "-l", "-b", "./" + TEMP_DIRECTORY])


def download_all_pdfs(links: List[Link]):
    for link in links:
        log("Downloading > " + link.name)
        download_pdf(link)
        log("Finished > " + link.name)


def main():
    while True:
        log("Create temp directory ...")
        create_temp_directory()
        log("Searching ...")
        links = get_links()
        download_all_pdfs(links)

        log("Converting to CSV with tabula ...")
        convert_to_csv()

        for link in links:
            headers = {'Content-type': 'application/json'}
            requests.post("http://localhost:8080/substitution/update",
                          data=convert_to_json(link, read_csv(link.get_csv_path())),
                          headers=headers)

        log("Deleting files ...")
        delete_temp_directory()
        log("Done. Sleeping for " + str(SLEEP) + "s")
        log("===================================================")
        time.sleep(SLEEP)


def read_csv(file_name):
    substitutions = []
    log("Reading > " + file_name)
    with open(file_name, newline='') as csv_file:
        for row in csv.reader(csv_file, delimiter=',', quotechar='"'):
            if row[0] == "St.":
                continue
            if row[0] == "Jg.":
                break

            lessons = row[0].split("-")

            if len(lessons) == 1:
                substitutions.append(Substitution(row))
            elif len(lessons) == 2:
                for i in range(int(lessons[0]), int(lessons[1]) + 1):
                    substitutions.append(Substitution([str(i), row[1], row[2], row[3], row[4], row[5]]))
            else:
                raise Exception("lessons length is not equal to 1 or 2")
    return sorted(substitutions, key=operator.attrgetter("lesson"))


if __name__ == "__main__":
    log("Booting ...")
    main()