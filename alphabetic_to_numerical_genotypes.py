import sys

replacement_dict = {
    'dd': '0',
    'Ad': '1',
    'AA': '2',
    'AB': '3',
    'BB': '4',
    'BC': '5',
    'M': '6'
}

if len(sys.argv) != 3:
    print("Usage: python alphabetic_to_numerical_genotypes.py <input_file.tsv> <output_file.tsv>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r') as f:
    lines = f.readlines()

with open(output_file, 'w') as f:
    for line in lines:
        columns = line.strip().split('\t')
        new_columns = [replacement_dict.get(col, col) for col in columns]
        new_line = '\t'.join(new_columns) + '\n'
        f.write(new_line)

print(f"Replacements done and saved to '{output_file}'")
