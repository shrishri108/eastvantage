# eastvantage

A small, approachable project that demonstrates loading a tiny sales dataset into a local SQLite database, transforming it with pandas, and exporting a simple CSV used for marketing analysis.

This repository contains two primary scripts:
- [create_database.py](create_database.py) — builds a local SQLite database and inserts sample data.
- [pandas_solution.py](pandas_solution.py) — reads the database, performs joins and aggregation with pandas, and writes `output/pandas_output.csv`.

## Prerequisites
- Python 3.8+ installed
- Git (optional, for cloning this repo)

## Install
1. Clone or download the repo.
2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

> If you run into issues with the package list, you can alternatively install `pandas` directly:

```bash
pip install pandas
```

## Run
1. Create the database and seed it with sample data:

```bash
python create_database.py
```

This creates `data/database.db` with the sample tables and rows.

2. Run the pandas transformation and export the CSV:

```bash
python pandas_solution.py
```

The script outputs `output/pandas_output.csv` (semicolon-separated) which contains aggregated quantities by customer and item for ages 18–35.

## Where to look next
- Example database schema and data generation logic: [create_database.py](create_database.py)
- Transformation and output logic: [pandas_solution.py](pandas_solution.py)
- Example SQL dump (if you prefer loading via SQL): `data/db_dump.sql`
- Test notebooks: `tests/database_test.ipynb` and `tests/database_test_with_new_db.ipynb`

## Notes
- The code is intentionally small and explicit to make it easy to follow. Feel free to fork and adapt the SQL schema, sample data, or pandas transformations.
- If you want the CSV to use commas instead of semicolons, edit the `to_csv` call in [pandas_solution.py](pandas_solution.py).

## Help / Next steps
If you want, I can:
- run the scripts here and show the resulting CSV,
- add a small unit test or a CLI wrapper, or
- change the output delimiter to comma and update the examples.

Enjoy!

