from typing import List
import json
import datetime

BASE_URL = "https://cms.sachsen.schule"
TEMP_DIRECTORY = "tmp"


class Link:

    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.date = Date(name)

    def get_url(self):
        return BASE_URL + self.path

    def get_pdf_path(self):
        return "./" + TEMP_DIRECTORY + "/" + self.name

    def get_csv_path(self):
        return "./" + TEMP_DIRECTORY + "/" + self.name.replace("pdf", "csv")

    def get_name(self):
        return self.name.replace(".pdf", "")


class Date:

    def __init__(self, file_name: str):
        parts = file_name.replace(".pdf", "").split("-")
        self.weekday = parts[0]
        self.year = parts[1]
        self.month = parts[2]
        self.day = parts[3]

    def get_timestamp(self):
        return (datetime.datetime(int(self.year), int(self.month), int(self.day))
                - datetime.datetime(1970, 1, 1)).total_seconds()

    def to_dictionary(self):
        return self.__dict__


class Substitution:

    def __init__(self, row: list):
        self.lesson = row[0]
        self.course = row[1]
        self.subject = row[2]
        self.teacher = row[3]
        self.room = row[4]
        self.info = row[5]
        self.id = 0

    def set_id(self, link: Link, index: int):
        self.id = link.get_name() + "_" + str(index)

    def to_dictionary(self):
        return self.__dict__


def convert_to_json(link: Link, substitutions: List[Substitution]):
    list_of_substitutions_as_dictionary = []
    index = 0
    for substitution in substitutions:
        substitution.set_id(link, index)
        list_of_substitutions_as_dictionary.append(substitution.to_dictionary())
        index += 1
    return json.dumps(
        {
            "id": link.get_name(),
            "year": int(link.date.year),
            "month": int(link.date.month),
            "day": int(link.date.day),
            "weekday": link.date.weekday,
            "timestamp": link.date.get_timestamp(),
            "substitutions": list_of_substitutions_as_dictionary
        })
