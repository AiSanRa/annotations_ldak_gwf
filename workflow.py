from gwf import Workflow

from templates import *

gwf = Workflow(defaults={"account": "put your account here"})

#Create the directories.
variants_file = "test_variants.txt"
genomes = [37, 38]
var = {37: gwf.glob("variants_37/*.vcf"), 38: gwf.glob("variants_38/*.vcf")}
gen = {37: gwf.glob("gtf_37/*.gtf"), 38: gwf.glob("gtf_38/*.gtf")}
exp = gwf.glob("expression/*.gct")
annot1 = gwf.glob("annot_37/*.txt")
annot2 = gwf.glob("annot_38/*.txt")
annot3 = gwf.glob("annot_chr_bp_37/*.txt")
annot4 = gwf.glob("annot_chr_bp_38/*.txt")
annot5 = gwf.glob("annot_all_chr_bp_37/*.txt")
annot6 = gwf.glob("annot_all_chr_bp_38/*.txt")

for genome in genomes:

    #Map the rs_IDs to get their chromosome and position.
    gwf.target(
        f'chr_pos_from_rsID_{genome}', 
        inputs=[variants_file] + var[genome], 
        outputs=[f"snp_chr_bp_{genome}.csv"], 
        memory="30g"
    ) <<f'''
    python code/snp_{genome}.py
    '''

    #Map using Chromosome and Position to get the Gene_IDs and rs_IDs.
    gwf.target(
        f'geneIDs_from_rsID_{genome}',
        inputs=[f"snp_chr_bp_{genome}.csv"] + gen[genome], 
        outputs=[f"geneID_{genome}.csv"],
        memory="4g" 
    ) <<f'''
    python code/geneID_{genome}.py
    '''

    #Map using Chromosome and Position to get the Gene_IDs and Chr:BP.
    gwf.target(
        f'geneID_from_rsID_to_chr_bp_{genome}', 
        inputs=[f"snp_chr_bp_{genome}.csv"] + gen[genome], 
        outputs=[f"geneID_chr_bp_{genome}.csv"], 
        memory="4g" 
    ) <<f'''
    python code/geneID_chr_bp_{genome}.py
    '''

    #Map using Chromosome and Position to get the Gene_IDs and Chr:BP from Chr:BP.
    gwf.target(
        f'geneID_from_chr_bp_{genome}', 
        inputs=["chr_bp.csv"] + gen[genome], 
        outputs=[f"geneID_all_chr_bp_{genome}.csv"], 
        memory="4g" 
    ) <<f'''
    python code/geneID_all_chr_bp_{genome}.py
    '''

#Split Chr:BP into Chr and BP.
gwf.target(
    f'chr_bp_split', 
    inputs=[variants_file], 
    outputs=["chr_bp.csv"], 
    memory="4g" 
) <<f'''
python code/chr_bp.py
'''

#Produce the annotation files from rs_IDs to rs_IDs GRCh37.
gwf.target(
    f'annotations_rsID_37', 
    inputs=["geneID_37.csv"] + exp, 
    outputs=annot1, 
    memory="4g" 
) <<f'''
python code/expression_37.py
'''

#Produce the annotation files from rs_IDs to rs_IDs GRCh38.
gwf.target(
    f'annotations_rsID_38', 
    inputs=["geneID_38.csv"] + exp, 
    outputs=annot2, 
    memory="4g" 
) <<f'''
python code/expression_38.py
'''

#Produce the annotation files from rs_IDs to Chr:BP GRCh37.
gwf.target(
    f'annotations_chr_bp_37', 
    inputs=["geneID_chr_bp_37.csv"] + exp, 
    outputs=annot3, 
    memory="4g" 
) <<f'''
python code/expression_chr_bp_37.py
'''

#Produce the annotation files from rs_IDs to Chr:BP GRCh38.
gwf.target(
    f'annotations_chr_bp_38', 
    inputs=["geneID_chr_bp_38.csv"] + exp, 
    outputs=annot4, 
    memory="4g" 
) <<f'''
python code/expression_chr_bp_38.py
'''

#Produce the annotation files from Chr:BP to Chr:BP GRCh37.
gwf.target(
    f'annotations_all_chr_bp_37', 
    inputs=["geneID_all_chr_bp_37.csv"] + exp, 
    outputs=annot5, 
    memory="4g" 
) <<f'''
python code/expression_all_chr_bp_37.py
'''

#Produce the annotation files from Chr:BP to Chr:BP GRCh38.
gwf.target(
    f'annotations_all_chr_bp_38', 
    inputs=["geneID_all_chr_bp_38.csv"] + exp, 
    outputs=annot6, 
    memory="4g" 
) <<f'''
python code/expression_all_chr_bp_38.py
'''