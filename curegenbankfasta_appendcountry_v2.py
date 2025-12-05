import os
import re
import time
from Bio import SeqIO
from Bio import Entrez

Entrez.email = "your_email@example.com"  # Replace with your email

def fetch_geo_location(genbank_id):
    """Fetch the geo-location for a given GenBank ID."""
    print(f"Fetching data for GenBank ID: {genbank_id}")  # Show the GenBank ID being processed
    try:
        time.sleep(0.5)  # Avoid rate limiting by NCBI
        handle = Entrez.efetch(db="nucleotide", id=genbank_id, rettype="gb", retmode="text")
        record = SeqIO.read(handle, "genbank")
        handle.close()  
        geo_location = ""
        for feature in record.features:
            if feature.type == 'source' and 'geo_loc_name' in feature.qualifiers:
                geo_location = feature.qualifiers['geo_loc_name'][0]
                print(f"Geo-location found: {geo_location}")  # Show the found geo-location
                break
    except Exception as e:
        print(f"Error fetching data for {genbank_id}: {e}")
    return geo_location

def process_file(file_name):
    """Process a single FASTA file to append geo-location information to sequence headers."""
    with open(file_name, 'r') as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        if line.startswith('>'):
            sample_name = line.strip()
            match = re.match(r">([A-Z0-9._]+)", sample_name)
            if match:
                genbank_id = match.group(1)
                geo_location = fetch_geo_location(genbank_id)
                sample_name = sample_name + f" {geo_location}\n" if geo_location else sample_name
            sample_name = re.sub(r'\b(?:large|subunit|and|complete|ITS2|ITS1|18S|small|fungus|spacer 1|spacer 2|genes|for|contains|clone|26S|partial|voucher|transcribed|sequence|rRNA|internal|uncultured|isolate|strain|ribosomal|spacer|gene|RNA|DNA|28S|25S|ITS|5.8S|from|material)\b', '', sample_name)
            sample_name = re.sub(r'[^a-zA-Z0-9]+', '_', sample_name).strip('_')
            sample_name = re.sub(r'_1_', '_', sample_name)  # Remove _1_ from the sample name
            cleaned_lines.append(f">{sample_name}\n")
        else:
            cleaned_lines.append(re.sub(r'\.1', '', line))

    file_name_without_ext = os.path.splitext(file_name)[0]
    with open(f"{file_name_without_ext}_cure.fasta", 'w') as f:
        for line in cleaned_lines:
            f.write(line)

    print(f"Done: see {file_name_without_ext}_cure.fasta")

def process_all_files():
    """Process all FASTA files in the current directory."""
    for file_name in os.listdir('.'):
        if file_name.endswith('.fasta') and '_cure' not in file_name:
            process_file(file_name)

def main():
    user_input = input("Enter the filename or 'all' to process all .fasta files in the folder: ")
    if user_input.lower() == 'all':
        process_all_files()
    else:
        if os.path.isfile(user_input):
            process_file(user_input)
        else:
            print("File not found.")

if __name__ == "__main__":
    main()