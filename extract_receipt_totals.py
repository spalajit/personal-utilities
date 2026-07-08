import os
import re
import argparse
from pathlib import Path
try:
    import PyPDF2
except ImportError:
    print("PyPDF2 not installed. Installing...")
    os.system("pip install PyPDF2")
    import PyPDF2

def extract_total_from_pdf(pdf_path):
    """Extract the grand total from a receipt PDF."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            # Common patterns for totals
            patterns = [
                r'Grand Total[:\s]+\$?([\d,]+\.?\d{0,2})',
                r'Order Total[:\s]+\$?([\d,]+\.?\d{0,2})',
                r'Total[:\s]+\$?([\d,]+\.?\d{0,2})',
                r'Amount Due[:\s]+\$?([\d,]+\.?\d{0,2})',
                r'Balance Due[:\s]+\$?([\d,]+\.?\d{0,2})',
                r'TOTAL[:\s]+\$?([\d,]+\.?\d{0,2})',
            ]

            # Try to find the total
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    # Get the last match (usually the final total)
                    amount_str = matches[-1].replace(',', '')
                    try:
                        return float(amount_str)
                    except:
                        continue

            return None
    except Exception as e:
        print(f"Error reading {pdf_path}: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Extract and total amounts from receipt PDFs.")
    parser.add_argument(
        "receipts_dir",
        nargs="?",
        default="./receipts",
        help="Path to the folder containing receipt PDFs (default: ./receipts)"
    )
    args = parser.parse_args()
    receipts_dir = args.receipts_dir

    totals = []
    failed = []

    # Walk through all PDF files
    for root, dirs, files in os.walk(receipts_dir):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                total = extract_total_from_pdf(pdf_path)

                if total is not None:
                    # Determine store from path
                    store = "Unknown"
                    if "Amazon" in pdf_path:
                        store = "Amazon"
                    elif "Home Depot" in pdf_path:
                        store = "Home Depot"
                    elif "Walmart" in pdf_path:
                        store = "Walmart"
                    elif "Wayfair" in pdf_path:
                        store = "Wayfair"

                    totals.append({
                        'file': file,
                        'path': pdf_path,
                        'total': total,
                        'store': store
                    })
                    print(f"[OK] {file}: ${total:.2f}")
                else:
                    failed.append(file)
                    print(f"[FAILED] {file}: Could not extract total")

    print("\n" + "="*80)
    print(f"\nSuccessfully processed: {len(totals)} receipts")
    print(f"Failed to process: {len(failed)} receipts")

    if totals:
        grand_total = sum(item['total'] for item in totals)

        # Calculate totals by store
        store_totals = {}
        for item in totals:
            store = item['store']
            if store not in store_totals:
                store_totals[store] = 0
            store_totals[store] += item['total']

        print(f"\n{'='*80}")
        print(f"BREAKDOWN BY STORE:")
        print(f"{'='*80}")
        for store in sorted(store_totals.keys()):
            print(f"{store}: ${store_totals[store]:,.2f}")

        print(f"\n{'='*80}")
        print(f"GRAND TOTAL (including tax): ${grand_total:,.2f}")
        print(f"{'='*80}\n")

    if failed:
        print("\nFailed receipts:")
        for f in failed:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
