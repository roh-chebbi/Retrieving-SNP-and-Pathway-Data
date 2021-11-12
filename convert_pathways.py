"""
convert_pathways.py - Python code to convert pathways data into a suitable format
For submission to NuGenomics - 12/11/2021

Summary:
    Input data is Pathways vs Genes
    Output data (desired) is Genes vs Pathways
    Code traverses the input data to make a list of genes present.
    Subsequently, it parses through the input data to get the 
    pathways associated with each gene.

Author:
    Rohini Chebbi
"""

import csv
import numpy as np

#Input and output csv filenames
filename_in= "Pathway_Gene.csv"
filename_out= 'PathOut.csv'

#Matrix for input rows
rows= []

with open(filename_in, 'r') as csvfile1: 
    #csv reader 
    csvreader = csv.reader(csvfile1) 
    for row in csvreader:
        rows.append(row) 

#Array to collect all gene names
all_genes=[]

for row in rows:
    row= [ row[0], row[1].split(",")]
    for element in row[1]:
        all_genes.append(element)

#Remove all duplicate genes from all_genes array
genes = []
[genes.append(x) for x in all_genes if x not in genes]

#Matrix for final data, gene vs pathways
data_out = np.empty([len(genes), 2], dtype=object)
data_out[:,0] = genes

#Adding pathway matches to each gene row
for generow in data_out:
    for row in rows:
        if generow[0] in row[1]:
            if generow[1]:
                generow[1]+= ', ' + row[0]
            else:
                generow[1]= row[0]

#Save data_out into output csv file
with open(filename_out, 'w') as csvfile2: 
    #csv writer 
    csvwriter = csv.writer(csvfile2) 
    for data in data_out:
        csvwriter.writerow(data)
