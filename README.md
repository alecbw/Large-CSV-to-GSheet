# Large-CSV-to-GSheet

A simple utility to upload large CSVs that break Google Sheet's importer. 

Documented Google Sheets service limits:

* 5 million cells
* 40,000 new rows at a time
* 18,278 columns
* 50,000 characters per cell
* [technically no row limit, but the cell limit will effectively limit you in the same way]

If you get the DOCUMENT_TOO_LARGE_TO_EDIT error, congrats, you have bricked your GSheet - IME this is caused by many cells with tens of thousands of characters

### Setup

```py
pip install gspread
```

### Usage

You'll need:
* a CSV you want to upload
* to edit the `.py` file to change `filename`, `gsheet_tab`, `gsheet_name`, and `start_at`

Start the execution with
```py
python3 upload_csv_to_gsheet.py
```

The script will batch the file into subsections (default 1000 rows) and iterate through the rows in batches of that number
