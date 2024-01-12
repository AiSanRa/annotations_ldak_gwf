import pandas as pd
import os
import sys
from scipy.stats import zscore

def read_expression_data(exp_file_path):
    exp_data = pd.read_csv(exp_file_path, skiprows=2, sep='\t', index_col=0, usecols=lambda x: x != 'Description')
    exp_data.index = exp_data.index.str.split('.').str[0]
    return exp_data

def read_variant_data(variant_file):
    variant_data = pd.read_csv(variant_file, usecols=[0, 1], names=[sys.argv[4], 'Gene_ID'])
    return variant_data

def match_gene_ids(variant_data, exp_data):
    # Match 'Gene_ID' column in variant_data with the first column of exp_data
    merged_data = pd.merge(variant_data, exp_data, left_on='Gene_ID', right_index=True)
    
    # Calculate the mean expression for each variant ID excluding 'Gene_ID' column
    merged_data_mean = merged_data.groupby(sys.argv[4], as_index=False).agg({col: 'mean' for col in merged_data.columns[2:]})
    return merged_data_mean

def z_standardize_data(merged_data):
    # Identify numeric columns excluding the first column
    numeric_columns = merged_data.iloc[:, 1:].select_dtypes(include=['float64', 'int64']).columns

    # Standardize each value using the mean and standard deviation of the entire dataset for numeric columns
    merged_data.loc[:, numeric_columns] = (merged_data.loc[:, numeric_columns] - merged_data.loc[:, numeric_columns].mean()) / merged_data.loc[:, numeric_columns].std()

    zscored_data = merged_data

def create_tissue_subfolders(zscored_data, output_folder):
    tissue_info = []
    for i, column in enumerate(zscored_data.columns[1:]):
        subfolder_name = f'tissue_{i + 1}'
        column_folder = os.path.join(output_folder, subfolder_name)
        os.makedirs(column_folder, exist_ok=True)

        subfolder_data = zscored_data[[sys.argv[4], column]]
        subfolder_data.to_csv(os.path.join(column_folder, 'bld66'), index=False, header=False, sep=('/t'))

        tissue_info.append({'tissue_name': column, 'tissue_folder': subfolder_name})

    return tissue_info

def save_tissue_info(tissue_info, output_folder):
    tissue_info_df = pd.DataFrame(tissue_info)
    tissue_info_df.to_csv(os.path.join(output_folder, 'tissue_info.csv'), index=False)

def process_data(variant_file, exp_file_path):
    output_folder = sys.argv[3]
    os.makedirs(output_folder, exist_ok=True)

    exp_data = read_expression_data(exp_file_path)
    variant_data = read_variant_data(variant_file)

    # Match 'Gene_ID' column in variant_data with the first column of exp_data
    merged_data = match_gene_ids(variant_data, exp_data)

    zscored_data = z_standardize_data(merged_data)

    zscored_data.to_csv(os.path.join(output_folder, 'zscored_data.csv'))

    tissue_info = create_tissue_subfolders(zscored_data, output_folder)

    save_tissue_info(tissue_info, output_folder)

# Example usage:
variant_file = sys.argv[1]
exp_file_path = sys.argv[2]
process_data(variant_file, exp_file_path)
