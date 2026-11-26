"""
E + L ของ ELT: อ่านไฟล์ CSV ของ Northwind จาก 2 ระบบ แล้วโหลดเข้า DuckDB
โดยไม่แก้ไขเนื้อหา

รันด้วย: python scripts/load_raw.py
"""

import sys
from pathlib import Path

# Load the installed duckdb package instead of the local scripts/duckdb.py entry
# point, which intentionally shares the package name.
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path = [
    entry
    for entry in sys.path
    if Path(entry or ".").resolve() != SCRIPTS_DIR
]

import duckdb


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = ROOT / "northwind.duckdb"

# ตารางใน schema raw และไฟล์ต้นทาง
SOURCES = {
    "customer": "raw/customer.csv",
    "employees": "raw/employees.csv",
    "orders": "raw/orders.csv",
    "order_details": "raw/order_details.csv",
    "products": "raw/products.csv",
    "shippers": "raw/shippers.csv",
    "suppliers": "raw/suppliers.csv",
    "legacy_orders": "legacy/orders.csv",
    "legacy_order_details": "legacy/order_details.csv",
}


def resolve_csv_path(relative_path: str) -> Path:
    csv_path = DATA_DIR / relative_path
    if csv_path.exists():
        return csv_path

    # รองรับชื่อโฟลเดอร์สะกดที่พบใน repository ตั้งต้น
    aliases = {
        "raw/customer.csv": ("raw/customer.csv", "rew/customer.csv"),
        "raw/employees.csv": ("raw/employees.csv", "rew/employees.csv"),
        "legacy/orders.csv": ("legacy/orders.csv", "legency/orders.csv"),
        "legacy/order_details.csv": (
            "legacy/order_details.csv",
            "legency/order_details.csv",
        ),
    }
    for alias in aliases.get(relative_path, (relative_path,)):
        candidate = DATA_DIR / alias
        if candidate.exists():
            return candidate

    return csv_path


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    con = duckdb.connect(str(DB_PATH))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")

        print(f"โหลดข้อมูลเข้า {DB_PATH.name}")
        for table, relative_path in SOURCES.items():
            csv_path = resolve_csv_path(relative_path)
            if not csv_path.exists():
                raise FileNotFoundError(f"ไม่พบไฟล์ {csv_path}")

            csv_literal = csv_path.as_posix().replace("'", "''")
            con.execute(
                f"""
                CREATE OR REPLACE TABLE raw.{table} AS
                SELECT *
                FROM read_csv('{csv_literal}', header = true)
                """
            )
            row_count = con.execute(
                f"SELECT COUNT(*) FROM raw.{table}"
            ).fetchone()[0]
            print(f" raw.{table:<22} {row_count:>6,} แถว")

        print("เสร็จแล้ว — ขั้นต่อไป: dbt run")
    finally:
        con.close()


if __name__ == "__main__":
    main()
