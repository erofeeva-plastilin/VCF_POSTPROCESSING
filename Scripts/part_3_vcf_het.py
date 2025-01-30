import time
import sys
import logging
from part_0_common import run_command, check_input_file, get_output_name

def run_heterozygosity_analysis(input_file):
    start_time = time.time()
    output_name = get_output_name(input_file)
    het_command = f"vcftools --vcf {input_file} --het --out {output_name}_het"
    run_command(het_command)
    logging.info(f"Heterozygosity data saved as {output_name}_het.het")
    execution_time = time.time() - start_time
    logging.info(f"Execution time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    input_file = check_input_file()
    run_heterozygosity_analysis(input_file)
