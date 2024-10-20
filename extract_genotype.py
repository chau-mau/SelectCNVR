import pandas as pd
import sys

if len(sys.argv) != 4:
    print("Usage: python extract_genotype.py <input_file.tsv> <output_file.tsv> <group_file.tsv>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
group_file = sys.argv[3]

print(f"Reading from: {input_file}")

try:
    df = pd.read_csv(input_file, sep="\t")
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

columns_to_keep = ['chr', 'start', 'end']
kmer_index = df.columns.get_loc('kmer')
average_index = df.columns.get_loc('average')
genotype_columns = df.columns[kmer_index + 1:average_index].tolist()
final_columns = columns_to_keep + genotype_columns

output_df = df[final_columns]
output_df.to_csv(output_file, sep='\t', index=False)

print(f"TSV file created: {output_file}")
