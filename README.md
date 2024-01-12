# Annotations for partitioned heritability in LDAK
Project for the master degree in bioinformatics (PiB) 2023, Aarhus Universitet.
This workflow proocess files with expression data to files usable as annotation files for LDAK.

# Overview
Workflow using gwf (https://gwf.app/#), a workflow tool for building and running large, scientific workflows. It runs on Python 3.7+ and is developed at GenomeDK, Aarhus University.
*EXPLICAR COMO FUNCIONA EL FLOW Y PONER UN DIAGRAMA

WARNING: this project was created and tested in the close cluster of iPSYCH. It should work perfectly fine outside the cluster but it was not tested.

# Requirements
Create a new environment to install gwf using conda.
For more information is highly recommended to go to the gwf install webpage: https://gwf.app/guide/tutorial/.

# Usage

Clone this repostory in the folder where you are going to work on.

    git clone https://github.com/AiSanRa/annotations_ldak_gwf.git

You should then prepare the files inside this folder:

- Copy your Variant_ids into the folder with the name "variants.txt".

**********************************
Now we should prepare the addicional folder that we might need for the process. This step is OPTIONAL but you must be aware that if you chose to use different files than the ones that are specified here you must:
- Be sure that the files have the same structure as the ones recommended: line split ("\t"), index of the ids, chromosome, position, etc in the same position, etc.
- This files must be inside the folders:
    - variants_37 or variants_38 for the first step to map Variant_Ids to chromosome and position.
    - gtf_37 or gtf_38, to map Variant_Ids to Gen_Ids.

- Create a folder called: "expression" and introduce your Expression file into the folder. Look at Additional Notes to know the structure that it must have.

After all the preparations are done and the requirements that we can see in the section Additional Notes have been met we can run our workflow. You might give your specific options to the workflow.\
**GRCh 37:**
- Input: rs_Id; Output: rs_Id

```bash
    gwf run annotations_rsID_37
```
- Input: rs_Id; Output: Chr:BP

```bash
    gwf run annotations_to_chr_bp_37
```

- Input: Chr:BP; Output: Chr:BP

```bash
    gwf run annotations_all_chr_bp_38
```

**GRCh 38:**

- Input: rs_Id; Output: rs_Id

```bash
    gwf run annotations_rsID_38
```

- Input: rs_Id; Output: Chr:BP

```bash
    gwf run annotations_to_chr_bp_38
```

- Input: Chr:BP; Output: Chr:BP

```bash
    gwf run annotations_all_chr_bp_38
```

Look at the progress of the pipeline.

    gwf status

# Additional Notes

- Your first input should always be called Variants.txt, doesnt matter the format the SNP_Ids (rs_Id or Chr:BP) are in. The file can containe additional information, but the Variant_ID must be in the first collumn without indexes. 
- You must be sure that before running the workflow you have the folders "variants_X" (This might not be needed if do not start with rsID), "gtf_X" and "expression".
- The Expression file must have a first collumn with the Gene_ID and next collumns should have the expression on different tissues. Each collumn, separated by line split("\t"), should have as index the name of the tissue or name you require.
- The option to have as an Input: Chr:BP and as an Output: rs_ID is not implemented in this workflow.
- This code is created to apply LDAK on it so the last output will be an annotation called bld66 inside a subfolder with the name of the tissue which can be identified in the tissue_info.csv.

# Acknowledgments