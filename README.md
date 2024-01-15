# Annotations for partitioned heritability in LDAK
Project for the master degree in bioinformatics (PiB) 2023/24, Aarhus Universitet.
This workflow proocess files with expression data to files usable as annotation files for LDAK.

# Overview
Workflow using gwf (https://gwf.app/#), a workflow tool for building and running large, scientific workflows. It runs on Python 3.7+ and is developed at GenomeDK, Aarhus University.

![Diagram of the annotations and tagging workflow.](https://github.com/AiSanRa/annotations_ldak_gwf/blob/main/diagram_workflow.jpg)
Diagram of the annotations and tagging workflow.

WARNING: this project was created and tested in the close cluster of iPSYCH. It should work perfectly fine outside the cluster but it was not tested.
SECOND WARNING: this workflow is not finished yet. There are some errors that are being in process to be fixed.

# Requirements
Create a new environment to install gwf using conda.
For more information is highly recommended to go to the gwf install webpage: https://gwf.app/guide/tutorial/.

# Usage

Clone this repostory.

    git clone https://github.com/AiSanRa/annotations_ldak_gwf.git

You should copy the workflow you want to use and also the code folder into your script folder or use the cloned folder.

Fill the config.py file with your options and the pathways that are needed.

Also, you will need to fill in the upper part of the workflow the name of your account: gwf = Workflow(defaults={"account": "put your account here"})

The workflows are constructed with gwf, to use them you simply have to run in the terminal where the script you want to execute is:

```bash
    gwf run 
```

Look at the progress of the pipeline.

    gwf status

# Additional Notes

- The option of input as Chr:BP and output as rs_ID is not implemented.
- All of the patways must be filled for the workflow to be successful.
- It is important to have the folder code in the folder where the script is.
- The workflow is created using the structure of the VCF and GTF files provided by Ensembl, so in case of using different ones the workflow might not work.
- The path to the VCF is to a folder that contains them all. However, the path in the configuration file to the GTF is to the file.
- During the mapping of variants, the workflow will just recognise the ones in the format that is specified in the configuration file. If the input file contains a mix of both some will be discarded.
- It has to be noticed that during the mapping of variant_IDs with gene_IDs some of the SNPs wont be included if they are intergenic SNPs, as they do not pertain to any gene.

# Acknowledgments

I would like to give the biggest acknowledge to my supervisor Jakob Grove for his patience, support and great kindness. I learned a lot in this project and a good part was thanks to his guide.
Also to all my partners and friends in Birc.
And finally, obviuosly, to me that I worked very hard on this and learned a lot from it.