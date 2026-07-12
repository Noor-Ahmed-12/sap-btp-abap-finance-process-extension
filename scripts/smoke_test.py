from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "python-client" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sap_finance_extension.cli import main


if __name__ == "__main__":
    print("Running offline smoke test...")
    main(["init"])
    main(["import-csv", str(ROOT / "sample-data" / "valid_invoices.csv")])
    main(["summary"])
    print("Smoke test completed.")
