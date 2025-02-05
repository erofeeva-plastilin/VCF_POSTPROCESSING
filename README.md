# VCF_POSTPROCESSING
## Installation
```
git clone https://github.com/erofeeva-plastilin/VCF_POSTPROCESSING.git
conda env create -f environment.yml
conda activate GWAS-PIPELINE
```
## Pipeline Components
### 💡 **part_0_common.py (Core Functions)**                    
This script contains common utility functions used across all other scripts:                   
- run_command() → Executes shell commands and logs outputs                   
- check_input_file() → Ensures the input VCF file is provided and exists                   
- get_output_name() → Generates standardized output file names based on the input VCF                   

### 💡 **part_1_vcf_pca_analysis.py (PCA Analysis)**                    
Performs Principal Component Analysis (PCA) on the VCF file:                   
- If >50 samples, runs plink2 for PCA directly                   
- If <50 samples, checks and fills missing variant IDs, computes allele frequencies, and then performs PCA                   
- Cleans up temporary logs (.log)                   
**Input:**                   
📄 *_vcf                   
**Output:**                   
📄 *_pca.eigenval, *_pca.eigenvec                      
(if <50 samples): *_pca.eigenval, *_pca.eigenvec, *_afreq, *_id.vcf                   
**Example:**                   
```
python3 part_1_vcf_pca_analysis.py {input}.vcf
```

### 💡 **part_2_vcf_distance_matrix.py (Genetic Distance Matrix)**                    
Computes genetic distance (1 - IBS) using plink 1.9:                   
- Runs plink --distance square **1-ibs** to generate the distance matrix                   
- Extracts sample IDs and converts results into a TSV format matrix                   
- Removes temporary log files (.log)                   
**Input:**                   
📄 *_vcf                   
**Output:**                   
📄 *_final_genetic_distances.tsv                   
*_mdist.id, *_mdist, *_nosex                   
**Example:**                   
```
python3 part_2_vcf_distance_matrix.py {input}.vcf
```

### 💡 **part_3_vcf_het.py (Heterozygosity Analysis)**                   
Analyzes heterozygosity levels for each sample using vcftools --het:                   
- Generates a heterozygosity report for quality control (vcftools)                   
- Deletes unnecessary log files (.log)                   
**Input:**                   
📄 *_vcf                   
**Output:**                   
📄 *_het.het                   
**Example:**                   
```
python3 part_3_vcf_het.py {input}.vcf
```

### 💡 **part_4_vcf_tree.py (Phylogenetic Tree Construction)**                   
Constructs a phylogenetic tree from the VCF file:                   
- Converts VCF to PHYLIP format (vcf2phylip)                   
- Runs IQ-TREE (iqtree2 -m GTR+G) to infer the tree structure                   
**Input:**                   
📄 *_vcf                   
**Output:**                   
📄 *_treefile, *_contree                   
*_phy, *_ckp.gz, *_iqtree, *_bionj,  *_mldist, *_splits.nex                    
**Example:**                   
```
python3 part_4_vcf_tree.py {input}.vcf
```

### 💡 **part_5_vcf_kinship.py (Kinship Matrix Calculation)**                   
Computes a KING-based kinship matrix using plink2 --make-king square:                   

- Extracts kinship coefficients from the .king file
- Converts the output into a TSV matrix format
- Deletes unnecessary log files (.log)                   
**Input:**                   
📄 *_vcf                   
**Output:**                   
📄 *_final_kinship.tsv                   
*_king.id, *_king                   
**Example:**                   
```
python3 part_5_vcf_kinship.py {input}.vcf
```
## Logs and data
Logs are stored in the "Logs" folder, while processed data is organized in the "Data" directory:
- test_data → Contains an example input VCF file (input.vcf)
- result_data → Includes examples of all generated output files from the pipeline

The logs folder is created automatically

## **Workflow**
The pipeline follows a structured sequence of preprocessing steps:
```mermaid
graph TD;
    A[Raw VCF] -->|Filtering| B[Filtered VCF]
    B --> C[Imputed VCF]
    B --> D[Filtered VCF (No Imputation)]
    C --> E[VCF with Unique IDs]
    D --> E[VCF with Unique IDs]
    E --> F[LD Pruned VCF]
    E --> G[Non-Pruned VCF]
    
    F --> H[Updated VCF (VCFv4.2)]
    G --> H[Updated VCF (VCFv4.2)]
    
    H --> I[Heterozygosity Report]
    H --> J[Kinship Matrix]
    H --> K[Distance Matrix]
    H --> L[PCA Output]
    H --> M[Phylogenetic Tree]
```
