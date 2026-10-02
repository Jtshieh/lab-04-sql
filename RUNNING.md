# Run the lab

Install Python 3.12 or later and uv, then run `uv sync` from this directory.
Set `DBHOST`, `DBUSER`, `DBPASS`, and `DBNAME` in your shell using your course
database credentials. Set `MYSQL_PWD` for mycli. Use your assigned media
database for the SQL scripts and your assigned mock database for Python.

## Media tables

```bash
uv run mycli -h "$DBHOST" -P 3306 -u "$DBUSER" -D "${DBUSER}_media" < initialize.sql
uv run mycli -h "$DBHOST" -P 3306 -u "$DBUSER" -D "${DBUSER}_media" < media_query.sql > media_results.txt
```

`initialize.sql` creates ten users and ten related posts. The query joins the
tables and selects posts with at least ten likes from members interested in
Science or Technology. `media_results.txt` contains the four matching posts.

## Mock data

`MOCK_DATA.csv` contains 200 synthetic Mockaroo records. `inspect_data.ipynb`
shows the column types, missing values, and SQL type mapping. Removing rows
with missing values leaves 172 records. The group counts are blue 38, gold 41,
green 42, and purple 51.

```bash
export DBNAME="${DBUSER}_mock"
uv run python src/sql_lab/process.py
uv run python src/sql_lab/query.py --group blue --groupby group
```

The loader creates `mock` and inserts complete records with parameterized
queries. Rerunning it with the same CSV leaves existing rows unchanged.
If the table contains different data, the loader stops so that the contents
can be inspected before replacement. The query script filters by `group`
and counts rows for a selected column.
