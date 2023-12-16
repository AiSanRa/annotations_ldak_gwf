import pandas as pd

def process_snp_file(input_file, output_file):
    # Read the input file into a DataFrame
    df = pd.read_csv(input_file, delimiter="\t", header=None, names=["Variani_ID", "chromosome_position"])

    # Split the column into two
    df[["Chromosome", "Position"]] = df["chromosome_position"].str.split(":", expand=True)

    # Create a new column Chr:BP
    df["Chr:BP"] = df["Chromosome"] + ":" + df["Position"]

    # Reorder the columns
    df = df[["Variani_ID", "Chr:BP", "Chromosome", "Position"]]

    # Write the result to the output file
    df.to_csv(output_file, sep=",", index=False)

input_file = "variants.txt"
output_file = "snp_chr_bp.csv"
process_snp_file(input_file, output_file)
