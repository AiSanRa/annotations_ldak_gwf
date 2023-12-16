#!/bin/bash
#SBATCH --partition normal
#SBATCH --account "enter your account name here"
#SBATCH --mem 80gb
#SBATCH -t 10:00:00

# Function to download and gunzip files
download_and_gunzip() {
    local folder=$1
    local urls=$2

    # Create the folder if it doesn't exist
    if [ ! -d "$folder" ]; then
        mkdir "$folder"
    fi

    # Read each URL from the string and download/gunzip
    IFS=', ' read -r -a url_array <<< "$urls"
    for url in "${url_array[@]}"; do
        # Extract the filename from the URL
        filename=$(basename "$url")

        # Download the file from the URL
        wget "$url" -O "$folder/$filename"

        # Decompress the file
        gunzip "$folder/$filename"
    done

    echo "Process completed for $folder"
}

# Read the commands.txt file for Expression files
while IFS= read -r line || [ -n "$line" ]; do
    # Check if the line contains "GRCh 37"
    if [[ "$line" == *"GRCh 37"* ]]; then
        folder_name="GTF_37"
        url="https://ftp.ensembl.org/pub/grch37/current/gtf/homo_sapiens/Homo_sapiens.GRCh37.87.gtf.gz"
    # Check if the line contains "GRCh 38"
    elif [[ "$line" == *"GRCh 38"* ]]; then
        folder_name="GTF_38"
        url="https://ftp.ensembl.org/pub/release-110/gtf/homo_sapiens/Homo_sapiens.GRCh38.110.gtf.gz"
    else
        echo "Unrecognized version in the line: $line"
        continue
    fi

    # Create the folder if it doesn't exist
    if [ ! -d "$folder_name" ]; then
        mkdir "$folder_name"
    fi

    # Extract the filename from the URL
    filename=$(basename "$url")

    # Download the file from the URL
    wget "$url" -O "$folder_name/$filename"

    # Decompress the file
    gunzip "$folder_name/$filename"

    echo "Process completed for $folder_name"
done < commands.txt

# Read the commands.txt file for VCF files
while IFS= read -r line || [ -n "$line" ]; do
    # Check if the line contains "GRCh 37"
    if [[ "$line" == *"GRCh 37"* ]]; then
        version_folder="Variants_37"
        urls="https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr1.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr2.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr3.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr4.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr5.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr6.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr7.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr8.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr9.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr10.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr11.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr12.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr13.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr14.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr15.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr16.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr17.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr18.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr19.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr20.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr21.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chr22.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chrMT.vcf.gz, https://ftp.ensembl.org/pub/grch37/current/variation/vcf/homo_sapiens/homo_sapiens-chrX.vcf.gz"
    # Check if the line contains "GRCh 38"
    elif [[ "$line" == *"GRCh 38"* ]]; then
        version_folder="Variants_38"
        urls="https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr1.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr2.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr3.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr4.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr5.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr6.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr7.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr8.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr9.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr10.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr11.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr12.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr13.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr14.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr15.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr16.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr17.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr18.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr19.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr20.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr21.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chr22.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chrMT.vcf.gz, https://ftp.ensembl.org/pub/grch38/current/variation/vcf/homo_sapiens/homo_sapiens-chrX.vcf.gz"
    else
        echo "Unrecognized version in the line: $line"
        continue
    fi

    # Download and gunzip files based on the version
    download_and_gunzip "$version_folder" "$urls"
done < commands.txt
