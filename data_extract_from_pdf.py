import pdfplumber
import pandas as pd
import re

def extract_gemeinde_data(pdf_path):
    """
    Extract Gemeindekennziffer and Gemeindename from Austrian municipality PDF
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        pandas.DataFrame: DataFrame with Gemeindekennziffer and Gemeindename
    """
    
    gemeinde_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"Processing page {page_num} of {len(pdf.pages)}")
            
            # Extract text from the page
            text = page.extract_text()
            
            if text:
                # Split text into lines
                lines = text.split('\n')
                
                for line in lines:
                    # Skip header lines and empty lines
                    if not line.strip() or 'Gemeindekennziffer' in line or 'Gemeindename' in line:
                        continue
                    
                    # Skip source attribution lines
                    if 'STATISTIK AUSTRIA' in line or 'Erstellt am' in line or 'Quelle:' in line:
                        continue
                    
                    # Pattern to match: 5-digit code followed by municipality name
                    # Example: "10101 Eisenstadt 10101 SR 7000"
                    match = re.match(r'^(\d{5})\s+([A-Za-zÄÖÜäöüß\s\-\.]+?)\s+\d{5}', line)
                    
                    if match:
                        gemeindekennziffer = match.group(1)
                        gemeindename = match.group(2).strip()
                        
                        gemeinde_data.append({
                            'Gemeindekennziffer': gemeindekennziffer,
                            'Gemeindename': gemeindename
                        })
    
    # Create DataFrame
    df = pd.DataFrame(gemeinde_data)
    
    # Remove duplicates (in case of any)
    df = df.drop_duplicates(subset=['Gemeindekennziffer'])
    
    # Sort by Gemeindekennziffer
    df = df.sort_values('Gemeindekennziffer').reset_index(drop=True)
    
    return df


def extract_gemeinde_data_advanced(pdf_path):
    """
    Advanced extraction using table detection
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        pandas.DataFrame: DataFrame with Gemeindekennziffer and Gemeindename
    """
    
    gemeinde_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"Processing page {page_num} of {len(pdf.pages)}")
            
            # Try to extract tables first
            tables = page.extract_tables()
            
            if tables:
                for table in tables:
                    for row in table:
                        # Skip header rows
                        if row[0] == 'Gemeinde' or row[0] == 'kennziffer' or not row[0]:
                            continue
                        
                        # Check if first column is a 5-digit number
                        if row[0] and re.match(r'^\d{5}$', str(row[0]).strip()):
                            gemeindekennziffer = row[0].strip()
                            gemeindename = row[1].strip() if len(row) > 1 and row[1] else ''
                            
                            if gemeindename:
                                gemeinde_data.append({
                                    'Gemeindekennziffer': gemeindekennziffer,
                                    'Gemeindename': gemeindename
                                })
    
    # Create DataFrame
    df = pd.DataFrame(gemeinde_data)
    
    if not df.empty:
        # Remove duplicates
        df = df.drop_duplicates(subset=['Gemeindekennziffer'])
        # Sort by Gemeindekennziffer
        df = df.sort_values('Gemeindekennziffer').reset_index(drop=True)
    
    return df


# Main execution
if __name__ == "__main__":
    # Specify your PDF file path
    pdf_file_path = "gemliste_knz.pdf"
    
    print("Method 1: Text-based extraction")
    print("=" * 50)
    df1 = extract_gemeinde_data(pdf_file_path)
    print(f"\nExtracted {len(df1)} municipalities")
    print("\nFirst 10 entries:")
    print(df1.head(10))
    
    print("\n\nMethod 2: Table-based extraction")
    print("=" * 50)
    df2 = extract_gemeinde_data_advanced(pdf_file_path)
    print(f"\nExtracted {len(df2)} municipalities")
    print("\nFirst 10 entries:")
    print(df2.head(10))
    
    # Choose the method that gives better results
    final_df = df2 if len(df2) > len(df1) else df1
    
    # Save to CSV
    output_file = "gemeinde_data.csv"
    final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n\nData saved to: {output_file}")
    
    # Save to Excel
    output_excel = "gemeinde_data.xlsx"
    final_df.to_excel(output_excel, index=False, engine='openpyxl')
    print(f"Data saved to: {output_excel}")
    
    # Display summary statistics
    print("\n\nSummary Statistics:")
    print("=" * 50)
    print(f"Total municipalities: {len(final_df)}")
    print(f"\nMunicipalities by Bundesland (first digit):")
    final_df['Bundesland_Code'] = final_df['Gemeindekennziffer'].str[0]
    print(final_df['Bundesland_Code'].value_counts().sort_index())