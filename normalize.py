import pandas as pd
import sys

def load_group_definitions(group_file):
    group_map = {}
    with open(group_file) as f:
        for line in f:
            individual, group_name = line.strip().split('\t')
            group_map[individual] = group_name
    return group_map

def load_column_groups(column_file):
    column_groups = []
    with open(column_file) as f:
        for line in f:
            range_str = line.split('#')[0].strip()  # Ignore comments
            if range_str:
                if '-' in range_str:
                    try:
                        start, end = map(int, range_str.split('-'))
                        column_groups.append(list(range(start - 1, end)))  # Convert to 0-based indexing
                    except ValueError:
                        print(f"Warning: Invalid range '{range_str}', skipping.")
                else:
                    individual_columns = [col.strip() for col in range_str.split(',')]
                    try:
                        indices = [int(col) - 1 for col in individual_columns if col.isdigit()]
                        column_groups.append(indices)
                    except ValueError:
                        print(f"Warning: Invalid column entries '{range_str}', skipping.")
    return column_groups

def normalize_data(df, column_groups):
    for group_columns in column_groups:
        print(f"Normalizing columns: {group_columns}")
        df.iloc[:, group_columns] = (df.iloc[:, group_columns] - df.iloc[:, group_columns].mean()) / df.iloc[:, group_columns].std()
    return df

if len(sys.argv) != 5:
    print("Usage: python normalize.py <input_file.tsv> <output_file.tsv> <group_file.tsv> <column_groups.txt>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
group_file = sys.argv[3]
column_file = sys.argv[4]

df = pd.read_csv(input_file, sep='\t')
group_map = load_group_definitions(group_file)
column_groups = load_column_groups(column_file)
df_normalized = normalize_data(df, column_groups)
df_normalized.to_csv(output_file, sep='\t', index=False)

print(f"Normalized TSV file created: {output_file}")
