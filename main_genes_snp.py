"""
main_genes_snp.py - Python code to get SNP metadata for each gene
For submission to NuGenomics - 12/11/2021

Summary:
    This code uses the Ensembl REST API (https://github.com/Ensembl/ensembl-rest/wiki) to
    access SNP information for the gene queried. The Ensembl REST API provides language 
    agnostic programmatic access to data on the Ensembl database. 

    This script uses the API and takes an input list of genes to get the SNP rsid, 
    major/minor allele, and location. Several python functions are defined to keep the 
    code modular. The output data is written into a csv file in a pre-specified format.  
    

Author:
    Rohini Chebbi
"""


import sys
import json
import time
import json
import csv

# Python 2/3 adaptability
try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError

class EnsemblRestClient(object):
    def __init__(self, server='http://rest.ensembl.org', reqs_per_sec=15):
        self.server = server
        self.reqs_per_sec = reqs_per_sec
        self.req_count = 0
        self.last_req = 0

    def perform_rest_action(self, endpoint, hdrs=None, params=None):
        if hdrs is None:
            hdrs = {}

        if 'Content-Type' not in hdrs:
            hdrs['Content-Type'] = 'application/json'

        if params:
            endpoint += '?' + urlencode(params)

        data = None

        # check if we need to rate limit ourselves
        if self.req_count >= self.reqs_per_sec:
            delta = time.time() - self.last_req
            if delta < 1:
                time.sleep(1 - delta)
            self.last_req = time.time()
            self.req_count = 0

        try:
            request = Request(self.server + endpoint, headers=hdrs)
            response = urlopen(request)
            content = response.read()
            if content:
                data = json.loads(content)
            self.req_count += 1

        except HTTPError as e:
            # check if we are being rate limited by the server
            if e.code == 429:
                if 'Retry-After' in e.headers:
                    retry = e.headers['Retry-After']
                    time.sleep(float(retry))
                    self.perform_rest_action(endpoint, hdrs, params)
            else:
                sys.stderr.write('Request failed for {0}: Status code: {1.code} Reason: {1.reason}\n'.format(endpoint, e))

        return data

    def get_variants(self, species, symbol):
        genes = self.perform_rest_action(
            endpoint='/xrefs/symbol/{0}/{1}'.format(species, symbol),
            params={'object_type': 'gene'}
        )
        if genes:
            stable_id = genes[0]['id']
            variants = self.perform_rest_action(
                '/overlap/id/{0}'.format(stable_id),
                params={'feature': 'variation'}
            )
            return variants
        return None

#takes gene as input and returns its variants
def run(species, symbol):
    client = EnsemblRestClient()
    variants = client.get_variants(species, symbol)
    if variants:
        return variants

#reads input csv file row by row and returns rows
def read_csv(input_filename):
    rows = []
    with open(input_filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
    
        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
    return rows

#writes SNP data to a csv file in a pre-specified format
def write_snp_csv(output_filename, gene_variants):
    # writing to csv file 
    with open(output_filename, 'a') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        
        for v in gene_variants:
            row = [v["id"], symbol, v["alleles"], str(v["start"]) + "-" + str(v["end"]), v["consequence_type"]]
            csvwriter.writerow(row)
            
#Main script which initializes all of the variables. Retrieves the SNPs for each gene using the REST API 
#and writes the output to a csv file             
if __name__ == '__main__':
    
    #configuration variables
    input_genes = []
    output_fields = ["SNP rsid", "Gene Name", "Allele", "Location (Start - End)", "Consequence Type"]
    input_filename = "Genes_Input.csv"
    output_filename = "Output_Genes.csv"
    species = "human"    
   
    #read input list of genes
    input_genes = read_csv(input_filename)

    #writes the headers in the output file
    with open(output_filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(output_fields)
        
    i = 0
    
    #retrieves SNP data for every gene in the input gene list
    for gene in input_genes:
        symbol = gene[0]
        gene_variants = run(species,symbol)

        if gene_variants:
            write_snp_csv(output_filename, gene_variants)
            i = i + 1
            print("Number of genes parsed..", i)
        else:
            print(symbol," is not present in ENSEMBL database")

        