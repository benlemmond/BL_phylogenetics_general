Purpose: this script cleans up genbank names, adds geographic metadata, and produces a fasta file called {filename)_cure.fasta that can be used in alignment programs without causing special character errors.

How to use this script:
Dependencies: python3, Biopython (install via anaconda)

Basic workflow:
BLAST a sequence and download results (automatic filename from genbank will be 'seqdump.txt')
Change this file extension to .fasta
Copy script to working directory containing one or more .fasta files 
run 'python curegenbankfasta_appendcountry_v2.py' {or 'python3 ...', depending on your python install)
you will be prompted to either specify a particular file (include .fasta extension) or just type 'all' to process all fasta files in working directory

Troubleshooting:
If 'Bio' package is not found, make sure you have installed 'Biopython' (e.g. 'conda install -c conda-forge biopython')
If the script does not run and no error is given, make sure that you actually were able to change the extension to '.fasta' from '.txt' (with MacOS computers, you have to go to Finder > Preferences > Advanced and enable 'Show all filename extensions'

Note that not all entries will have associated geographic data, and some extraneous words may remain
