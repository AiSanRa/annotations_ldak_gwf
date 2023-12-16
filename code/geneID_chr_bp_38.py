import os
import csv

def parse_exp(exp_file):
    gene_dict = {}
    with open(exp_file, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            fields = line.strip().split('\t')
            if fields[2] == 'gene':
                attributes = fields[8].split(';')
                gene_id = [attr.split(' ')[-1].strip('"') for attr in attributes if 'gene_id' in attr][0]
                start = int(fields[3])
                end = int(fields[4])
                chromosome = fields[0]
                gene_dict[gene_id] = {'start': start, 'end': end, 'chromosome': chromosome}
    return gene_dict

def process_csv(exp_dict, csv_file):
    result = set()
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            chr_bp = row['Chr:BP']
            position = int(row['Position'])
            chromosome = row['Chromosome']
            for gene_id, gene_info in exp_dict.items():
                if gene_info['chromosome'] == chromosome and gene_info['start'] <= position <= gene_info['end']:
                    result.add((chr_bp, gene_id))
    return result

def write_output(output_file, result):
    with open(output_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Chr:BP', 'Gene_ID'])
        for chr_bp, gene_id in result:
            csv_writer.writerow([chr_bp, gene_id])

if __name__ == '__main__':
    csv_file = 'snp_chr_bp_38.csv'
    folder_path = 'gtf_38/'
    output_file = 'geneID_chr_bp_38.csv'


#This part could be changed to be an option, but for now it is ok.
    exp_dict = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt') or filename.endswith('.gtf'):
            exp_file_path = os.path.join(folder_path, filename)
            exp_dict.update(parse_exp(exp_file_path))

    result = process_csv(exp_dict, csv_file)
    write_output(output_file, result)