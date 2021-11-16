# Retrieving SNP and Pathway Data
This project includes the code for the following tasks: 

Given a list of genes, 
1. Retrieve their SNPs with the respective rsids, variant alleles and locations based on GRCh38/hg38 
2. All pathways associated with each gene

Table of Contents
=================

   * [Retrieving SNP and Pathway Data](#Retrieving-SNP-and-Pathway-Data)
      * [1. Retrieving SNP metadata](#1-Retrieving-SNP-metadata)
      * [2. Genes vs Pathways](#1-Genes-vs-Pathways)

## Retrieving SNP metadata
This code uses the [Ensemble REST API](https://github.com/Ensembl/ensembl-rest/wiki) to access SNP information for the gene queried. The Ensembl REST API 
provides language agnostic programmatic access to data on the Ensembl database. 

The code is present in ```main_genes_snp.py```, where each function is explained. 

The input is ```Genes_Input.csv```.


## Genes vs Pathways
The [DAVID database](https://david.ncifcrf.gov/) was used to get pathway for the query gene list. DAVID provides a comprehensive set of 
functional annotation tools for investigators to understand biological meaning behind large list of genes.
The gene list was queried with the background Homo sapien. Under 'GOTERM_BP_DIRECT', KEGG data was downloaded and hits of p value > 0.05 
were discarded. As the downloaded file was in the form Pathways vs Genes, a python script was used to convert it into the form of Genes vs Pathways.

The code is present in ```convert_pathways.py```.

The input is ```Pathway_Gene.com``` (after excel manipulation). 

## Notes
1. Out of 595 genes, only 215 genes had pathway hits after querying in DAVID.
2. Input data for retrieving SNP data was manually trimmed for whitespaces.
3. Out of 595 genes, x number were not found in the Ensemble database.
4. In ```main_genes_snp.py```, type of variant is also included as a header in the output csv file.

## Author
Rohini Chebbi 
