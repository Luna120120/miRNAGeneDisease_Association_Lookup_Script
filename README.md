# miRNA-Gene-Disease Association Lookup Script

## Description
This Python script provides a powerful tool for searching a database containing associations between **microRNAs (miRNAs)**, **diseases**, and **genes**. 

It offers two functions:

**1. Searching:** 
The user can search for diseases associated with a given miRNA name, or miRNAs associated with a given disease name, based on the **miRNA-Gene association score (mirna_score)** or/and **Gene-Disease association score (gene_score)**. Results including and above the score thresholds will be filtered as output.

- **Input:**  a miRNA name (**mirna**) or a disease name (**disease**) ( Optional: **mirna_score**, **gene_score** )
- **Output**: A table containing filtered miRNA, genes and disease.
  
***Example:***
`python mian_script.py -m hsa-miR-101-3p -ms 90 -gs 0.9`

```plaintext
The file is loaded: "miRNA_disease_linked.csv".

Matching diseases associated to the input miRNA when:
   miRNA score >= 90.0
   gene_score >= 0.9

Here are the associated [Diseases] and [Genes] to the input [miRNA]: "hsa-miR-101-3p"

|      | miRNA          | diseaseName                                | geneSymbol   |
|-----:|:---------------|:-------------------------------------------|:-------------|
|  936 | hsa-miR-101-3p | charcot-marie-tooth disease, type 4b1      | MTMR2        |
|  937 | hsa-miR-101-3p | epilepsy                                   | SCN8A        |
|  939 | hsa-miR-101-3p | endocrine-cerebroosteodysplasia            | CILK1        |
|  940 | hsa-miR-101-3p | loeys-dietz syndrome                       | TGFBR1       |
```

`python mian_script.py -d "alzheimer's disease" -ms 99 -gs 0.90`

```plaintext
The file is loaded: "miRNA_disease_linked.csv".

Matching miRNAs associated to the input disease where:
   miRNA score >= 98.0
   gene_score >= 0.9

Here are the associated [miRNAs] and [Genes] to the input [Disease]: "alzheimer's disease"

|       | miRNA           | diseaseName         | geneSymbol   |
|------:|:----------------|:--------------------|:-------------|
|    52 | hsa-let-7a-3p   | alzheimer's disease | APP          |
|   215 | hsa-let-7b-3p   | alzheimer's disease | APP          |
|   586 | hsa-let-7f-1-3p | alzheimer's disease | APP          |
| 20683 | hsa-miR-4422    | alzheimer's disease | APP          |
| 20684 | hsa-miR-4422    | alzheimer's disease | APP          |
```

**2. Browsing:** 
The user can **browse** the database for matches to given **query**, which will be one or a part of a miRNA or disease name. 

- **Input:** The browse type (**"mirna"** or **"disease"**) and the query ( **partial or full miRNA/disease name** )
- **Output:** A list containing all the matched miRNA or disease results.
  
***Example:***
`python mian_script.py -b mirna -q hsa-miR-101`

```plaintext

The file is loaded: "miRNA_disease_linked.csv".

    The browsing type is 'mirna' 
    The query you entered is 'hsa-miR-101'

Here are 3 miRNA names that match your query:

['hsa-miR-101-2-5p' 'hsa-miR-101-3p' 'hsa-miR-101-5p']
```

`python mian_script.py -b disease -q "type III"`

```plaintext

The file is loaded: "miRNA_disease_linked.csv".

    The browsing type is 'disease' 
    The query you entered is 'type III'

Here are 5 miRNA names that match your query:

osteogenesis imperfecta type iii (disorder)
glycogen storage disease type iii
tyrosinemia, type iii
usher syndrome, type iii
leukocyte adhesion deficiency, type iii
```

## Requirements
- Python 3
- Pandas library

## Usage Instructions

### Basic Commands
- `-f, --file`: the path to the CSV file serving as the database (default: "miRNA_disease_linked.csv")
- `-m, --mirna`: the miRNA name to search for
- `-d, --disease`: the disease name to search for
- `-ms, --mirna_score`: the threshold for miRNA-Gene association score (mirna_score) (default: 80)
- `-gs, --gene_score`: the threshold for Gene-Disease association score (gene_score) (default: 0.8)
- `-b, --browse`: the browse type (input "mirna" or "disease")
- `-q, --query`: the query string for browsing
- `-e, --example`: show example usage.

### Notes
- This script requires at least one name to function search. It can only search for one (miRNA or disease) name at a time. Multiple-word disease names must be enclosed in quotes.
- The valid ranges of mirna_score and gene_score are 80-100 and 0.8-1.0. If not specified, the script will search for relevant miRNA or disease by the default scores (80 and 0.8).
- The browsing function requires a valid query. If browsing one or a partial name, the browsing type (mirna or disease) must be specified.


### Examples Usage
##### Search by miRNA:
- Search for diseases related to a specific miRNA with default scores:
  `python script-name.py -m hsa-miR-892c-5p`
- Search for diseases with specified scores:
  `python script-name.py -m hsa-miR-892c-5p -ms 95`
  `python script-name.py -m hsa-miR-892c-5p -ms 95 -gs 0.9`
##### Search by diseases:
- Search for miRNAs related to a single-word disease name with a score threshold:
  `python script-name.py -d obesity -ms 0.95`
- Search for miRNAs related to a multiple-word disease name with score thresholds:
  `python script-name.py -d "liver carcinoma" -ms 95 -gs 0.95`
##### Browse query:
-	Browse miRNAs match the query "let-7":
`python script-name.py -b mirna -q let-7`
-	Browse diseases match the query contains multiple words:
`python script-name.py -b disease -q "type 1"`


## Error Handling
The script has custom error handling for scenarios like missing files, multiple name entries, conflicting searches, scores outside the valid range, missing names, unspecified browsing types, and names not found in the database.

## Extensibility
The script is designed to be adaptable. Users can easily switch the database file and adjust score thresholds as needed.

