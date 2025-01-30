import time
import os
import sys
import logging
import pandas as pd
from part_0_common import run_command, check_input_file, get_output_name

def run_genetic_distance_analysis(input_file):
    start_time = time.time()
    output_name = get_output_name(input_file)
    dist_command = f"plink --vcf {input_file} --distance square 1-ibs --out {output_name}_genetic_distances"
    run_command(dist_command)
    logging.info(f"Genetic distance matrix saved as {output_name}_genetic_distances.mdist")
    plink_log_file = f"{output_name}_genetic_distances.log"
    if os.path.exists(plink_log_file):
        os.remove(plink_log_file)
    id_file = f"{output_name}_genetic_distances.mdist.id"
    dist_file = f"{output_name}_genetic_distances.mdist"
    if not os.path.exists(id_file) or not os.path.exists(dist_file):
        logging.error(f"PLINK output files not found ({id_file} or {dist_file})")
        sys.exit(1)
    sample_ids = pd.read_csv(id_file, sep=r'\s+', header=None, usecols=[0], engine='python')[0].tolist()
    df = pd.read_csv(dist_file, sep=r'\s+', header=None, engine='python')
    if len(sample_ids) != df.shape[0]:
        logging.error(f"Mismatch: {len(sample_ids)} samples, but {df.shape[0]} rows in distance matrix")
        sys.exit(1)
    df.index = sample_ids
    df.columns = sample_ids
    output_tsv = f"{output_name}_final_genetic_distances.tsv"
    df.to_csv(output_tsv, sep="\t")
    logging.info(f"Final genetic distance matrix saved as {output_tsv}")
    execution_time = time.time() - start_time
    logging.info(f"Execution time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    input_file = check_input_file()
    run_genetic_distance_analysis(input_file)
