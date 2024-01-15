import pandas as pd
import sys

def process_chromosome_position(input_file, output_file):
    # Read the tab-delimited text file into a pandas DataFrame
    df = pd.read_csv(input_file, delimiter="\t", header=None, names=["chromosome_position"])

    # Split the "chromosome_position" column into "Chromosome" and "Position" columns
    df[["Chromosome", "Position"]] = df["chromosome_position"].str.split(":", expand=True)

    # Concatenate "Chromosome" and "Position" into a new column "Chr:BP"
    df["Chr:BP"] = df["Chromosome"] + ":" + df["Position"]

    # Reorder the columns to have "Chr:BP", "Chromosome", and "Position"
    df = df[["Chr:BP", "Chromosome", "Position"]]

    # Save the DataFrame to a new CSV file with comma as the delimiter
    df.to_csv(output_file, sep=",", index=False)

# Example usage
input_file = sys.argv[1]
output_file = sys.argv[2]
process_chromosome_position(input_file, output_file)
