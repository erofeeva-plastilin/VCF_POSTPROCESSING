import time
import os
import logging
import pandas as pd
from part_0_common import run_command, check_input_file, get_output_name

def run_pca_analysis(input_file):
    start_time = time.time()
    output_name = get_output_name(input_file)
    sample_count = int(run_command(f"bcftools query -l {input_file} | wc -l").strip())
    logging.info(f"Sample count: {sample_count}")
    if sample_count >= 50:
        logging.info("Sample count ≥ 50. Running PCA directly.")
        pca_command = f"/mnt/tools/plink2_2024/plink2 --vcf {input_file} --pca --out {output_name}_pca"
    else:
        logging.info("Sample count < 50. Checking for missing IDs and calculating allele frequencies.")
        id_check_command = f"bcftools view -H {input_file} | cut -f3 | grep -E '^\\.$' | wc -l"
        missing_ids = int(run_command(id_check_command).strip())
        if missing_ids > 0:
            logging.info(f"Detected {missing_ids} missing IDs. Filling missing IDs...")
            annotated_file = f"{output_name}_id.vcf"
            run_command(f"bcftools annotate -Oz --set-id +'%CHROM:%POS:%REF:%ALT' -o {annotated_file} {input_file}")
            input_file = annotated_file
        freq_file = f"{output_name}_freq"
        logging.info("Generating allele frequency file...")
        run_command(f"/mnt/tools/plink2_2024/plink2 --vcf {input_file} --freq --out {freq_file}")
        pca_command = f"/mnt/tools/plink2_2024/plink2 --vcf {input_file} --pca --out {output_name}_pca --read-freq {freq_file}.afreq"

    run_command(pca_command)
    plink_log_file = f"{output_name}_pca.log"
    freq_log_file = f"{freq_file}.log"
    for log_file in [plink_log_file, freq_log_file]:
        if os.path.exists(log_file):
            os.remove(log_file)
    logging.info(f"PCA completed successfully. Results saved in {output_name}_pca")
    execution_time = time.time() - start_time
    logging.info(f"Execution time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    input_file = check_input_file()
    run_pca_analysis(input_file)
