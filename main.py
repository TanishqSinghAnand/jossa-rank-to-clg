import pdfplumber
import pandas as pd
import os

def is_valid_rank(val):
    try:
        int(val)
        return True
    except:
        return False

def extract_clean_josaa_data(pdf_path):
    output_csv = os.path.join(os.path.dirname(pdf_path), "josaa_data.csv")
    data = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            print(f"Processing page {i+1}...")
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row and row[0] is not None and len(row) == 7:
                        opening = row[5].strip() if row[5] else ''
                        closing = row[6].strip() if row[6] else ''
                        if is_valid_rank(opening) and is_valid_rank(closing):
                            cleaned_row = [col.strip() if col else '' for col in row]
                            data.append(cleaned_row)

    columns = [
        "Institute Name", "Academic Program", "Quota",
        "Seat Type", "Gender", "Opening Rank", "Closing Rank"
    ]
    
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_csv, index=False)
    print(f"\n✅ Cleaned CSV saved to: {output_csv} with {len(df)} rows")

# Your PDF path
pdf_path = r"D:\Coding\Python\JOSSA\JoSAA.pdf"
extract_clean_josaa_data(pdf_path)
