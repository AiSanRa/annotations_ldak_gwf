from gwf import Workflow

from templates import *
from config import *

import os

gwf = Workflow(defaults={"account": "put your account here"})

bim = f"{plink_path}.bim"
bed = f"{plink_path}.bed"
fam = f"{plink_path}.fam"


subfolders = [os.path.join(annot,f) for f in os.listdir(annot) if os.path.isdir(os.path.join(annot, f))]
for line in subfolders:
    subfolder = line.strip()
    tissue = os.path.basename(subfolder)
    all_bld_files = gwf.glob(os.path.join(subfolder,"bld*"))
    #Exclude the fil named bld66.
    filtered_bld_files = [file for file in all_bld_files if "bld66" not in file]

    gwf.target(
        f'links_categories_{tissue}', 
        inputs=subfolder, 
        outputs=filtered_bld_files, 
        memory="30g",
        walltime="00:30:00",
        cores=8,
    ) <<f'''
    python {scriptdir}/code/bld.sh {annot} {bld_path}
    '''

    gwf.target(
        f'links_tagging_files_{tissue}', 
        inputs=filtered_bld_files, 
        outputs=[f'{subfolder}/tags.sh'], 
        memory="30g",
        walltime="00:30:00",
        cores=8,
    ) <<f'''
    bash {scriptdir}/code/link_tag_script.sh {subfolder} {scriptdir}
    '''

   gwf.target(
        f'create_tags_{tissue}', 
        inputs=[bim, bed, fam, f'{subfolder}/tags.sh'] + all_bld_files, 
        outputs=[f'{subfolder}/{name}.tagging', f'{subfolder}/done_tagging], 
        memory="30g",
        walltime="00:50:00",
        cores=8,
    ) <<f'''
    cd {subfolder}
    sbatch {subfolder}/tags.sh {name} {plink_path}
    '''