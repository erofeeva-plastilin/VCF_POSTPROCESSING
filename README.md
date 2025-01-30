# VCF_POSTPROCESSING
## Installation
```
git clone https://github.com/erofeeva-plastilin/VCF_POSTPROCESSING.git
conda activate GWAS-PIPELINE
```
## Pipeline Components
1️⃣ **part_0_common.py (Core Functions)**                    
This script contains common utility functions used across all other scripts:                   
- run_command() → Executes shell commands and logs outputs                   
- check_input_file() → Ensures the input VCF file is provided and exists                   
- get_output_name() → Generates standardized output file names based on the input VCF                   

2️⃣ **part_1_vcf_pca_analysis.py (PCA Analysis)**                    
Performs Principal Component Analysis (PCA) on the VCF file:                   
- If >50 samples, runs plink2 for PCA directly                   
- If <50 samples, checks and fills missing variant IDs, computes allele frequencies, and then performs PCA                   
- Cleans up temporary logs (.log)                   
**Input:**                   
📄 *_.vcf                   
**Output:**                   
📄 *_pca.eigenval, *_pca.eigenvec                       
*_afreq, *_id.vcf (+ if <50 samples)                   
**Example:**                   
```
python3 part_1_vcf_pca_analysis.py {input}.vcf
```

3️⃣ **part_2_vcf_distance_matrix.py (Genetic Distance Matrix)**                    
Computes genetic distance (1 - IBS) using plink 1.9:                   
- Runs plink --distance square **1-ibs** to generate the distance matrix                   
- Extracts sample IDs and converts results into a TSV format matrix                   
- Removes temporary log files (.log)                   
**Input:**                   
📄 *_.vcf                   
**Output:**                   
📄 *_final_genetic_distances.tsv                   
*_.mdist.id, *_.mdist                   
**Example:**                   
```
python3 part_2_vcf_distance_matrix.py {input}.vcf
```

4️⃣ **part_3_vcf_het.py (Heterozygosity Analysis)**                   
Analyzes heterozygosity levels for each sample using vcftools --het:                   
- Generates a heterozygosity report for quality control (vcftools)                   
- Deletes unnecessary log files (.log)                   
**Input:**                   
📄 *_.vcf                   
**Output:**                   
📄 *_het.het                   
**Example:**                   
```
python3 part_3_vcf_het.py {input}.vcf
```

5️⃣ **part_4_vcf_tree.py (Phylogenetic Tree Construction)**                   
Constructs a phylogenetic tree from the VCF file:                   
- Converts VCF to PHYLIP format (vcf2phylip)                   
- Runs IQ-TREE (iqtree2 -m GTR+G) to infer the tree structure                   
**Input:**                   
📄 *_.vcf                   
**Output:**                   
📄 *.treefile, *.contree                   
*_.phy, *_.ckp.gz, *_.iqtree, *_.bionj,  *_.mldist, *_.splits.nex                    
**Example:**                   
```
python3 part_4_vcf_tree.py {input}.vcf
```

6️⃣ **part_5_vcf_kinship.py (Kinship Matrix Calculation)**                   
Computes a KING-based kinship matrix using plink2 --make-king square:                   

- Extracts kinship coefficients from the .king file
- Converts the output into a TSV matrix format
- Deletes unnecessary log files (.log)                   
**Input:**                   
📄 *_.vcf                   
**Output:**                   
📄 *_final_kinship.tsv                   
*_.king.id, *_.king                   
**Example:**                   
```
python3 part_5_vcf_kinship.py {input}.vcf
```
## Logs and data
Logs are stored in the "Logs" folder, while processed data is organized in the "Data" directory:
- test_data → Contains an example input VCF file (input.vcf)
- result_data → Includes examples of all generated output files from the pipeline
