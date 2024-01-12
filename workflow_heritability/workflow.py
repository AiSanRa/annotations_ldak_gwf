from gwf import Workflow

from templates import *
from config import *

import os

gwf = Workflow(defaults={"account": "put your account here"})

name= ""

subfolders = [os.path.join(annot,f) for f in os.listdir(annot) if os.path.isdir(os.path.join(annot, f))]
for line in subfolders:
    subfolder = line.strip()
    tissue = os.path.basename(subfolder)

    gwf.target(
        f'links_sumher_files_{tissue}', 
        inputs=[f'{scriptdir}/code', subfolder], 
        outputs=[f'{subfolder}/sums.sh'], 
        memory="30g",
        walltime="00:30:00",
        cores=8,
    ) <<f'''
    bash {scriptdir}/code/link_sums_script.sh  {scriptdir}/code {subfolder}
    '''

   gwf.target(
        f'sumher_{tissue}', 
        inputs=[f'{subfolder}/sums.sh'], 
        outputs=[f'{subfolder}/{name}.enrich', f'{subfolder}/done_heritability], 
        memory="30g",
        walltime="25:00:00",
        cores=8
    ) <<f'''
    cd {subfolder}
    sbatch {subfolder}/sums.sh {name} {sumsstats} {name}
    '''