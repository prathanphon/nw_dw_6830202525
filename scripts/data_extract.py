"""Entry point for the Northwind raw data extraction."""

try:
    from .load_raw import main
except ImportError:
    from load_raw import main


if __name__ == "__main__":
    main()
