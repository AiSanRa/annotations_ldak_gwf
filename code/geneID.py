import os
import csv

def find_gtf_file(folder):
    for file in os.listdir(folder):
        if file.endswith('.gtf'):
            return os.path.join(folder, file)
    return None

def parse_gtf(gtf_file):
    gene_dict = {}
    with open(gtf_file, 'r') as file:
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

def process_csv(gtf_dict, csv_file):
    result = set()
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            variant_id = row[sys.argv[4]
            position = int(row['Position'])
            chromosome = row['Chromosome']
            for gene_id, gene_info in gtf_dict.items():
                if gene_info['chromosome'] == chromosome and gene_info['start'] <= position <= gene_info['end']:
                    result.add((variant_id, gene_id))
    return result

def write_output(output_file, result):
    with open(output_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Variant_ID', 'Gene_ID'])
        for variant_id, gene_id in result:
            csv_writer.writerow([variant_id, gene_id])

if __name__ == '__main__':
    csv_file = sys.argv[1]
    gtf_file = sys.argv[2]
    output_file = sys.argv[3]
    
    gtf_dict = parse_gtf(gtf_file)
    result = process_csv(gtf_dict, csv_file)
    write_output(output_file, result)