this project stores a small SQLite database in `/data/` and includes scripts and tests
to validate and produce a simple marketing-analysis CSV.

Prereqs
- Python 3.12
- Install requirements:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Database and tests
- The database file lives in `/data/database.db`.
- Run the tests in the `tests` folder to verify database integrity before running solutions. If integrity checks fail, try the repository's recovery steps; if recovery fails, recreate the DB with [create_database.py](create_database.py).

Useful files
- `pandas_solution.py`: solution implemented using pandas only.
- `sql_solution.py`: solution implemented using pure SQL against the database. You can run queries with the included SQLite binary as an alternative:

```bash
./tests/sqlite3.exe ./data/database.db
```

Then paste your query from `sql_solution.csv` or  `sql_solution.py`.
- `sql_solution.csv`: stores query test output using `;` as delimiter (implemented because instruction 3 was unclear; both CSV and `sql_solution.py` are provided).

Quick run
1. Ensure `data/database.db` exists (or create it):

```bash
python create_database.py
```

2. Run the pandas solution:

```bash
python pandas_solution.py
```

Output files are stored in `/output` folder