from sys import maxsize
import csv
import config
import logging
from os.path import exists

NUMBER_OF_KEYS_PER_CONFIG = 24

KEYS_TO_TRY = ['config']
for k in config.PATHS.keys():
    for i in range(NUMBER_OF_KEYS_PER_CONFIG):
        KEYS_TO_TRY.append("{}{}".format(k, i))

maxInt = maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt / 10)


def readfile(filename, fields=None):
    lines = []
    with open(filename, "r", encoding="utf-8") as csvFile:
        reader = csv.DictReader(csvFile, fields)
        for row in reader:
            lines.append(row)
    return lines


def readfile_low_memory(filename):
    lines = []
    with open(filename, "r", encoding="utf-8") as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            lines.append(row)
    return lines


def writeToCsv(data, name, fields=None):
    logger = logging.getLogger(__name__)
    if len(data) >= 1:
        logger.info("saving: data")
        if fields is None:
            field = list(data[0].keys())
        else:
            field = fields

        with open("{}.csv".format(name), "a", newline="", encoding="utf-8") as csvfile:

            writer = csv.DictWriter(
                csvfile, fieldnames=field, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for d in data:
                writer.writerow(d)
    else:
        logger.info("no data found")


def check_name(name, debug=True, limit=15) -> str:
    new_name = name
    count = 0
    while exists("{}.csv".format(new_name)):
        new_name = f"{name}{count}"
        count += 1
        if debug:
            print(f"{name}{count}.csv already exists trying alternative name")
        if count > limit:
            return ""
    return new_name


def get_latest_name(name) -> str:
    new_name = name
    count = 0
    while exists("{}.csv".format(new_name)):
        new_name = f"{name}{count}"
        count += 1

        if count > 10:
            return f"{name}{count-2}.csv"

    # if the file doesn't exist return empty
    if count == 0:
        return ""

    if count == 1:
        return f"{name}.csv"

    return f"{name}{count - 2}.csv"
