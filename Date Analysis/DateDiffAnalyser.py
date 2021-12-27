import csv
import matplotlib.pyplot as plt
import statistics
import collections
import numpy as np

# This script analyzes the date difference between MITRE date and NVD date
# and MITRE date and EDB Date

def get_date_diff(db):
    date_diff = []
    for entry in db:
        # if int(entry[3]) > -2000:
        date_diff.append(int(entry[3]))
    return date_diff


def count_freqs(db):
    negative_freq = 0
    positive_freq = 0
    zero_freq = 0

    for entry in db:
        if entry == 0:
            zero_freq = zero_freq + 1

        if entry > 0:
            positive_freq = positive_freq + 1

        if entry < 0:
            negative_freq = negative_freq + 1

    print("Number of negative: ", negative_freq)
    print("Number of positive: ", positive_freq)
    print("Number of zero: ", zero_freq)

def get_date_diff_counts(db):
    counts = {}

    for entry in db:
        if int(entry[3]) in counts:
            counts[int(entry[3])] = counts[int(entry[3])] + 1
        else:
            counts[int(entry[3])] = 1

    return counts


def find_max_date_diff(db):
    max_date_diff = -99999

    for entry in db:
        if max_date_diff < int(entry[3]):
            max_date_diff = int(entry[3])

    return max_date_diff


def find_min_date_diff(db):
    min_date_diff = 99999

    for entry in db:
        if min_date_diff > int(entry[3]):
            min_date_diff = int(entry[3])

    return min_date_diff


def find_avg_date_diff(db):
    date_diff_sum = 0

    for entry in db:
        date_diff_sum = date_diff_sum + int(entry[3])

    return date_diff_sum / len(db)


def create_db(db_file_name):
    db = []
    with open(db_file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        next(csv_reader)  # skip field row

        for row in csv_reader:
            if row[3] != '':  # date_diff is not null
                db.append([row[0], row[1], row[2], row[3]])

    return db


def analyze(db_file_name):
    db = create_db(db_file_name)

    print("--------------------------------------------------")
    print("File Name: " + db_file_name)
    db_date_diff_list = get_date_diff(db)  # get the date diff as a list
    db_date_diff_list.sort()
    print("number of dataset: " + str(len(db_date_diff_list)))
    print("max date diff: " + str(max(db_date_diff_list)) + " days")
    print("min date diff: " + str(min(db_date_diff_list)) + " days")
    print("avg date diff: " + str(statistics.mean(db_date_diff_list)) + " days")
    print("median date diff: " + str(statistics.median(db_date_diff_list)) + " days")
    print("mode date diff: " + str(statistics.median(db_date_diff_list)) + " days")
    print("multi mode date diff: " + str(statistics.multimode(db_date_diff_list)) + " days")
    print("median low date diff: " + str(statistics.median_low(db_date_diff_list)) + " days")
    print("median high diff: " + str(statistics.median_high(db_date_diff_list)) + " days")
    count_freqs(db_date_diff_list)
    print(db_date_diff_list)

    db_date_date_diff_counts = get_date_diff_counts(db)
    orderd_db_counts = collections.OrderedDict(sorted(db_date_date_diff_counts.items()))
    print(orderd_db_counts)
    print("------------------------------")
    # plot_histogram(db_date_diff_list, db_file_name)
    # plot_dot_graph(orderd_db_counts, db_file_name)
    plot_bar_graph(orderd_db_counts, db_file_name)



def plot_histogram(db_date_diff_list, db_file_name):
    fig, ax = plt.subplots(1, 1)
    db_date_diff_list_np = np.array(db_date_diff_list)
    # ax.hist(db_date_diff_list_np, bins=100, range=(-90, 90))
    ax.hist(db_date_diff_list_np, bins=300)

    if db_file_name == "../Files/mitre_nvd_db.csv":
        ax.set_title("MITRE and NVD Date Diff")
        ax.set_xlabel("Date Diff (Days) = NVD Date - MITRE Date")
    elif db_file_name == "./Files/mitre_edb_db.csv":
        ax.set_title("MITRE and EDB Date Diff")
        ax.set_xlabel("Date Diff (Days) = EDB Date - MITRE Date")
    elif db_file_name == "../Files/zdi_nvd_db.csv":
        ax.set_title("ZDI and NVD Date Diff")
        ax.set_xlabel("Date Diff (Days) = ZDI Date - NVD Date")
    elif db_file_name == "../Files/edb_zdi.csv":
        ax.set_title("EDB and ZDI Date Diff")
        ax.set_xlabel("Date Diff (Days) = EDB Date - ZDI Date")

    ax.set_ylabel("Frequency")
    # plt.show()

def plot_dot_graph(orderd_db_counts, db_file_name):
    # print(db_date_diff_list)
    x = []
    y = []
    for key, value in orderd_db_counts.items():
        x.append(key)
        y.append(value)
    # print(x)
    # print(y)
    fig, ax = plt.subplots(1,1)
    ax.scatter(x, y)

def plot_bar_graph(orderd_db_counts, db_file_name):
    # print(db_date_diff_list)
    x = []
    y = []
    for key, value in orderd_db_counts.items():
        if key >= -90 and key <= 90:
            x.append(key)
            y.append(value)

    fig, ax = plt.subplots(1, 1)
    ax.bar(x, y)

    if db_file_name == "../Files/mitre_nvd_db.csv":
        ax.set_title("MITRE and NVD Date Diff")
        ax.set_xlabel("Date Diff (Days) = NVD Date - MITRE Date")
    elif db_file_name == "./Files/mitre_edb_db.csv":
        ax.set_title("MITRE and EDB Date Diff")
        ax.set_xlabel("Date Diff (Days) = EDB Date - MITRE Date")
    elif db_file_name == "../Files/zdi_nvd_db.csv":
        ax.set_title("ZDI and NVD Date Diff")
        ax.set_xlabel("Date Diff (Days) = ZDI Date - NVD Date")
    elif db_file_name == "../Files/edb_zdi.csv":
        ax.set_title("EDB and ZDI Date Diff")
        ax.set_xlabel("Date Diff (Days) = EDB Date - ZDI Date")

    ax.set_ylabel("Frequency")

mitre_nvd_db_file = "../Files/mitre_nvd_db.csv"
mitre_edb_db_file = "../Files/mitre_edb_db.csv"
zdi_nvd_db_file = "../Files/zdi_nvd_db.csv"
edb_zdi_db_file = "../Files/edb_zdi.csv"

# analyze(mitre_nvd_db_file)
# analyze(mitre_edb_db_file)
analyze(zdi_nvd_db_file)
# analyze(edb_zdi_db_file)

plt.show()