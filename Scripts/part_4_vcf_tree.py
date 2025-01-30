import time
import sys
import os
import logging
from ete3 import PhyloTree, TreeStyle
from part_0_common import run_command, check_input_file, get_output_name

def run_phylogenetic_analysis(input_file):

    start_time = time.time()
    output_name = get_output_name(input_file)
    output_dir = os.path.dirname(input_file)
    temp_phy = f"{os.path.basename(output_name)}.min4.phy"
    output_phy = f"{output_name}.min4.phy"
    run_command(f"/mnt/tools/vcf2phylip/vcf2phylip.py -i {input_file} -o {temp_phy}")
    if os.path.exists(temp_phy):
        os.rename(temp_phy, output_phy)
        logging.info(f"PHYLIP matrix moved to {output_phy}")
    else:
        logging.error(f"ERROR: PHYLIP file {temp_phy} not found!")
        sys.exit(1)

    output_tree = f"{output_name}.min4.phy.contree"
    run_command(f"/mnt/tools/iqtree-2.3.6-Linux-intel/bin/iqtree2 -s {output_phy} -m GTR+G -nt 10 -st DNA -bb 1000")
    logging.info(f"Tree saved as {output_tree} (Newick format)")

    execution_time = time.time() - start_time
    logging.info(f"Execution time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    input_file = check_input_file()
    run_phylogenetic_analysis(input_file)
