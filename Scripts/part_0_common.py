import os
import sys
import subprocess
import logging
from datetime import datetime

script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = f"logs/VCF_POSTPROCESSING_{script_name}_{current_date}.log"
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        output = result.stdout.strip()
        error = result.stderr.strip()
        if output:
            logging.info(f"[STDOUT] {output}")
        if error:
            logging.warning(f"[STDERR] {error}")
        return output
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e.stderr.strip()}")
        sys.exit(1)

def check_input_file():
    if len(sys.argv) < 2:
        logging.error("Using: script.py <input_file.vcf>")
        sys.exit(1)

    input_file = os.path.abspath(sys.argv[1])
    if not os.path.exists(input_file):
        logging.error(f"Error: file {input_file} not found")
        sys.exit(1)
    return input_file

def get_output_name(input_file):
    return os.path.abspath(os.path.splitext(input_file)[0])
