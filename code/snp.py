import os
import csv
import sys
from glob import glob

def process_variant_files(var_folder, output_file, variant_ids_file):
    # Load variant ids into a set
    with open(variant_ids_file, "r") as f:
        # Read only the first column
        variant_ids = set(x.strip().split()[0] for x in f.readlines())

    # Define the columns for the result DataFrame
    result_columns = ["Variant_ID", "Chr:BP", "Chromosome", "Position"]

    # Open the output file for writing
    with open(output_file, "w", newline='') as output_csv:
        # Create a CSV writer
        csv_writer = csv.writer(output_csv)

        # Write the header to the CSV file
        csv_writer.writerow(result_columns)

        # Initialize a counter for debugging
        matched_variants = 0

        # Iterate through VCF variant files using glob
        var_files = glob(os.path.join(var_folder, "*.vcf"))
        for var_file_path in var_files:
            with open(var_file_path, "r") as var_file:
                for line in var_file:
                    if not line.startswith("#"):
                        fields = line.strip().split("\t")
                        chromosome, position, variant_id = fields[:3]

                        if variant_id in variant_ids:
                            result_row = [variant_id, f"{chromosome}:{position}", chromosome, position]
                            csv_writer.writerow(result_row)
                            matched_variants += 1

        print(f"Number of matched variants: {matched_variants}")

# Specify your input and output files
var_folder = sys.argv[2]
output_file = sys.argv[3]
variant_ids_file = sys.argv[1]

# Process variant files and write the result to the output file
process_variant_files(var_folder, output_file, variant_ids_file)

