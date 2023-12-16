import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

def process_data(variant_file):
    # Define the path to the Expression folder
    expression_folder = 'expression'

    # List all files in the Expression folder
    expression_files = os.listdir(expression_folder)

    # Filter for any file in the folder (remove the extension filter)
    exp_file = next(file for file in expression_files)

    # Construct the full path to the GCT file
    exp_file_path = os.path.join(expression_folder, exp_file)

    # Read GCT file excluding the 'Description' column
    exp_data = pd.read_csv(exp_file_path, skiprows=2, sep='\t', index_col=0, usecols=lambda x: x != 'Description')

    # Process the indices to remove numbers after the dot
    exp_data.index = exp_data.index.str.split('.').str[0]

    # Read variant file, skipping the first row
    variant_data = pd.read_csv(variant_file, usecols=[0, 1], names=['Chr:BP', 'Gene_ID'])

    # Create the 'Annotations' folder if it doesn't exist
    output_folder = 'annot_all_chr_bp_38'
    os.makedirs(output_folder, exist_ok=True)

    # DataFrame to store information about tissues
    tissue_info = pd.DataFrame(columns=['Tissue_Folder', 'Tissue_Header'])

    # Iterate through each tissue column in the file
    for i, tissue in enumerate(exp_data.columns, start=1):
        # Merge data frames based on processed gene IDs
        merged_data = pd.merge(variant_data, exp_data[[tissue]], left_on='Gene_ID', right_index=True)

        # Group by Chr:BP and calculate the mean of the expression values for each gene
        aggregated_data = merged_data.groupby('Chr:BP')[tissue].mean().reset_index()

        # Standardize the TPMS values across all samples
        scaler = StandardScaler()
        aggregated_data[tissue] = scaler.fit_transform(aggregated_data[[tissue]])

        # Create the subfolder inside 'annot_all_chr_bp_37' with the name of the tissue
        tissue_folder = os.path.join(output_folder, f"tissue_{i}")
        os.makedirs(tissue_folder, exist_ok=True)

        # Create the output file path inside the tissue subfolder
        output_file = os.path.join(tissue_folder, 'bld66')

        # Write data to the output file
        aggregated_data.to_csv(output_file, sep='\t', index=False, header=False)

        # Add information about the tissue to the DataFrame
        tissue_info = pd.concat([tissue_info, pd.DataFrame({'Tissue_Folder': [f'tissue_{i}'], 'Tissue_Header': [tissue]})], ignore_index=True)

    # Save the tissue information to a CSV file
    tissue_info.to_csv(os.path.join(output_folder, 'tissue_info.csv'), index=False)

if __name__ == "__main__":
    variant_file_path = 'geneID_all_chr_bp_38.csv'

    process_data(variant_file_path)
