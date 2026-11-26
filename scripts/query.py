"""Run a read-only query against the Northwind DuckDB database."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
DB_PATH = ROOT / "northwind.duckdb"

# scripts/duckdb.py is a local entry point; exclude it while importing the
# installed DuckDB package.
sys.path = [path for path in sys.path if Path(path or ".").resolve() != SCRIPTS]
sys.path.insert(0, str(ROOT))

import duckdb


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    sql = " ".join(sys.argv[1:]).strip()
    if not sql:
        sql = "SHOW TABLES"

    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        result = con.execute(sql)
        if result.description:
            columns = [column[0] for column in result.description]
            print("\t".join(columns))
            for row in result.fetchall():
                print("\t".join("" if value is None else str(value) for value in row))
    finally:
        con.close()


if __name__ == "__main__":
    main()
