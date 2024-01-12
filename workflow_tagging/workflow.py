from gwf import Workflow

from templates import *
from config import *

import os

gwf = Workflow(defaults={"account": "put your account here"})

name = os.path.basename(variants)
annot = f"{scriptdir}/annotations_{name}"
new_bld = gwf.glob(f"annotations_{name}/tissue_*/bld66")

#Map the rs_IDs to get their chromosome and position.
gwf.target(
    f'chr_pos_from_rsID_{name}', 
    inputs=[variants, chr_bp_path], 
    outputs=[f"snp_chr_bp_{name}"], 
    memory="30g",
    walltime="00:30:00",
    cores=8,
) <<f'''
python {scriptdir}/code/snp.py {variants} {chr_bp_path} snp_chr_bp_{name}
'''

if input_format == "Variant_ID":
    #Map using Chromosome and Position to get the Gene_IDs and rs_IDs.
    gwf.target(
        f'geneIDs_from_rsID_{name}',
        inputs=[f"snp_chr_bp_{name}", gen_id], 
        outputs=[f"geneID_{name}"],
        memory="4g",
        walltime="00:30:00",
        cores=8,
    ) <<f'''
    python {scriptdir}/code/geneID.py snp_chr_bp_{name} {gen_id} geneID_{name} {variant_format_output}
    '''

elif input_format == "Chr:BP":
    #Split Chr:BP into Chr and BP.
    gwf.target(
        f'chr_bp_split', 
        inputs=[variants_file], 
        outputs=[f"geneID_{name}"], 
        memory="4g",
        walltime="00:30:00",
        cores=8, 
    ) <<f'''
    python {scriptdir}/code/chr_bp.py {variants} geneID_{name}
    '''

else:
    print("Error: input_format is not valid. Please use Variant_ID or Chr:BP.")


#Produce the annotation files.
gwf.target(
    f'annotations_{name}', 
    inputs=[f"geneID_{name}", exp], 
    outputs=nwe_bld, 
    memory="120g",
    walltime="00:30:00",
    cores=8,  
) <<f'''
python {scriptdir}/code/expression.py geneID_{name} {exp} annotations_{name} {variant_format_output}
'''