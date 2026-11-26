"""Command-line entry point for loading the Northwind CSV files into DuckDB."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent

# Remove scripts/ from the import path before loading the DuckDB package.
# Otherwise this file's name can shadow the installed duckdb module.
sys.path = [path for path in sys.path if Path(path or ".").resolve() != SCRIPTS]
sys.path.insert(0, str(ROOT))

import duckdb  # noqa: F401

sys.path.insert(0, str(SCRIPTS))
from load_raw import main


if __name__ == "__main__":
    main()
