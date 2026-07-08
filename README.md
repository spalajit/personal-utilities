# Personal Utilities

A collection of useful Python scripts for personal productivity and automation.

## Scripts

### extract_receipt_totals.py

Extracts and totals amounts from receipt PDFs across multiple stores.

**Features:**
- Automatically scans PDF receipts in a directory structure
- Extracts grand totals using intelligent pattern matching
- Organizes by store (Amazon, Walmart, Home Depot, Wayfair)
- Provides breakdown by store and overall grand total
- Reports success/failure for each file

**Usage:**
```bash
# Install dependencies
pip install PyPDF2

# Run against a folder of receipt PDFs (defaults to ./receipts if omitted)
python extract_receipt_totals.py /path/to/receipts
```

**Output:**
```
[OK] receipt1.pdf: $45.99
[OK] receipt2.pdf: $127.50
[FAILED] receipt3.pdf: Could not extract total

Successfully processed: 2 receipts
Failed to process: 1 receipts

BREAKDOWN BY STORE:
Amazon: $45.99
Walmart: $127.50

GRAND TOTAL (including tax): $173.49
```

**Requirements:**
- Python 3.6+
- PyPDF2

## Installation

```bash
# Clone the repository
git clone git@github.com:spalajit/PersonalUtilities.git
cd PersonalUtilities

# Install dependencies
pip install -r requirements.txt
```

## Adding New Utilities

When adding new scripts:
1. Add a descriptive docstring
2. Update this README with usage instructions
3. Add any dependencies to requirements.txt

## License

MIT
