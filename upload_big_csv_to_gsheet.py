from utility.util_gspread import *

import csv
import sys
import logging
from time import sleep

import gspread


###################################################################################################

def read_csv_as_lol(filename, **kwargs):
    filename = filename + ".csv" if ".csv" not in filename else filename

    with open(filename, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        file_lol = list(csv_reader)

    if kwargs.get("start_at"):
        file_lol = file_lol[kwargs["start_at"]:]

    return file_lol


def append_lol_to_gsheet_tab(sheet, tab, data_lol):

    sh, worksheet_list = open_gsheet(sheet)
    try:
        resp = sh.values_append(tab, {'valueInputOption': 'USER_ENTERED'}, {'values': data_lol})
        print(resp)

    except gspread.exceptions.APIError as e:
        logging.error(e)
        if "This document is too large to continue editing." in str(e) or "Unable to parse range:" in str(e):
            sys.exit(e)


###################################################################################################################

if __name__ == "__main__":

    csv.field_size_limit(100000000)

    start_at = 0
    filename = "Datafile.csv"
    gsheet_tab = "Uplaod_Tab"
    gsheet_name = "GSpread Testing Sheet"

    input_lol = read_csv_as_lol(
        filename,
        start_at=start_at,
    )

    batch_lol = []
    for n, row in enumerate(input_lol):
        if len(max(row, key=len)) > 49999:
            row = [x[:49998] for x in row]
            print('trimmed row')

        batch_lol.append(row)

        if n != 0 and n % 500 == 0:
            logging.info(f"We are now on row {n + start_at}")
            append_lol_to_gsheet_tab(gsheet_name, gsheet_tab, batch_lol)
            sleep(0.5)
            batch_lol = []


