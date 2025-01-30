import time
import logging
import os
import sys
import pandas as pd
from part_0_common import run_command, check_input_file, get_output_name

def run_kinship_analysis(input_file):
    start_time = time.time()
    output_name = get_output_name(input_file)
    kinship_command = f"plink2 --vcf {input_file} --allow-extra-chr --make-king square --out {output_name}_kinship"
    run_command(kinship_command)
    logging.info(f"Kinship matrix saved as {output_name}_kinship.king")
    plink_log_file = f"{output_name}_kinship.log"
    if os.path.exists(plink_log_file):
        os.remove(plink_log_file)
    id_file = f"{output_name}_kinship.king.id"
    kinship_file = f"{output_name}_kinship.king"
    if not os.path.exists(id_file) or not os.path.exists(kinship_file):
        logging.error(f"PLINK2 output files not found ({id_file} or {kinship_file})")
        sys.exit(1)
    sample_ids = pd.read_csv(id_file, sep=r'\s+', header=None, skiprows=1, usecols=[0], engine='python')[0].tolist()
    df = pd.read_csv(kinship_file, sep=r'\s+', header=None, engine='python')
    if len(sample_ids) != df.shape[0]:
        logging.error(f"Mismatch: {len(sample_ids)} samples, but {df.shape[0]} rows in kinship matrix")
        sys.exit(1)
    df.index = sample_ids
    df.columns = sample_ids
    output_tsv = f"{output_name}_final_kinship.tsv"
    df.to_csv(output_tsv, sep="\t")
    logging.info(f"Final kinship matrix saved as {output_tsv}")
    execution_time = time.time() - start_time
    logging.info(f"Execution time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    input_file = check_input_file()
    run_kinship_analysis(input_file)
