import re, sys, os 
import pandas as pd 
import argparse

#---------------------------------------------------------------------------------------------------------
# Print an instruction for user 
text_1 = " INFORMATION "    # add a border line 
print(f'\n{text_1:-^100}')
welcome = '" Welcome to use the miRNA-Gene-Disease Association Lookup tool ! "'
print(f'\n{welcome: ^100}')


print('\nDESCRIPTION: \n') 
print('This tool has 2 function:\n')
print('1. Search a miRNA [-m] or disease [-d] to look up the associated diseases or miRNAs, based on two thresholds: \n   "miRNA-Gene association score" (mirna_score) and "Gene-Disease association score" (gene_score). \n   Associated genes will also be given.')
print('2. Browse [-d] a query [-q] (one or a partial miRNA/disease name) to see all possible names in the database.')
print('\nNOTES: \n') 
print('1. The default input file using as the database is "merged_cleaned_data.csv.csv".\n   Use "-f" to change database.')
print('2. The default threshold of "mirna_score" and "gene_score" are 80 and 0.8.\n   Use "-ms" and "-gs" to change values in ranges [80 - 100] and [0.8 - 1.0] for finer search.')
print('3. If performing function 1, one miRNA or disease name is required as input. \n   Notice, the program can only look up for one query at a time, so please only provide one name in one searching.')
print('4. If performing function 2, one query and a specified browse type are required as inputs.')
print('5. If the input name is longer than 1 word, it must be enclosed it by " " to avoid errors.')
print('\n- Use "-e" to see example usage.') 
print('\n- Use "-h" to see all the arguments.\n') 

text_2 = " OUTPUT "         # add a border line 
print(f'{text_2:-^100}\n') 

#---------------------------------------------------------------------------------------------------------
# Setup parser
parser = argparse.ArgumentParser(description='functions: Lookup database for miRNA, gene, and disease associations.')
parser.add_argument('-f', '--file', type=str, 
                    help='the path to the CSV file as the database', 
                    default="merged_cleaned_data.csv")
parser.add_argument('-m', '--mirna', nargs="*", 
                    help='the miRNA name to search for')
parser.add_argument('-d', '--disease', nargs="*", 
                    help='the disease name to search for')
parser.add_argument('-ms', '--mirna_score', type=float, 
                    default=80, 
                    help='the threshold for miRNA-Gene association score (mirna_score)')
parser.add_argument('-gs', '--gene_score', type=float, 
                    default=0.8, 
                    help='the threshold for Gene-Disease association score (gene_score)')
parser.add_argument('-b', '--browse', type=str, 
                    help='the browse type (input "mirna" or "disease")')
parser.add_argument('-q', '--query', type=str, 
                    help='the query string for browsing')
parser.add_argument('-e', '--example', action='store_true',
                    help='show example usage')

#---------------------------------------------------------------------------------------------------------
# Creating exception classes
class SearchConflictError(Exception):
    """Exception raised when both miRNA and disease names are provided."""
class InvalidScoreError(Exception):
    """Custom exception for invalid miRNA scores or gene score."""

class MissingNameError(Exception):
    """Custom exception for missing miRNA or disease query."""

class MissingBrowseTypeError(Exception):
    """Custom exception for missing browse type when query is provided."""

class NameNotFoundError(Exception):
    """Exception raised when miRNA name is not found in the database."""

class MatchNotFoundError(Exception):
    """Exception raised when no matches are found for a query in the database."""

#---------------------------------------------------------------------------------------------------------
# Defining error trapping functions

# Checking input file
def validate_file(file_path):
    """Check if the given file exists."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'\nFile not found: "{file_path}".\nPlease check the file path and try again.\n')
    else:
        print(f'The file is loaded as database: "{file_path}".\n')
        return True

# Checking the type and size of the mirna_score/gene_score
def validate_scores(mirna_score, gene_score):
    """Validate miRNA and gene scores."""
    if not isinstance(mirna_score, (int, float)) or mirna_score < 80 or mirna_score > 100:
        raise InvalidScoreError('\nInvalid miRNA score. Enter a number in range [80 - 100].')
    if not isinstance(gene_score, (int, float)) or gene_score < 0.8 or gene_score > 1.0:
        raise InvalidScoreError('\nInvalid gene score. Enter a number in range [0.8 - 1.0].')

# Requesting a miRNA/disease name when the mirna_score or/and the gene_score are given 
def validate_names_and_scores(mirna, disease, browse, query):
    """Validate query and scores."""
    if not mirna and not disease and not browse and not query:
        raise MissingNameError('\nA miRNA name or a disease name must be provided when scores are given.')

# Requesting a browse type when a query is entered
def validate_browse_and_query(browse, query):
    """Validates that the browse type is provided when a query is given."""
    if query and not browse:
        raise MissingBrowseTypeError('\nPlease specify a browse type (mirna or disease) when a query is given.')

# Trapping non existing mirna/disease name
# --- miRNA
def check_mirna_name(df, mirna):
    """Check miRNA name in the database."""
    if mirna:
        mirna_name = mirna[0]
        if mirna_name not in df['miRNA'].values:
            raise NameNotFoundError(f'\n"{mirna_name}" did not find in database. \nPlease check your flag type (-m for miRNA, -d for disease) and enter a valid name.')
        return df[df['miRNA'] == mirna_name]
    return None

# --- disease
def check_disease_name(df,disease):
    """Check disease name in the database."""
    if disease:
        disease_name = disease[0]
        if disease_name not in df['diseaseName'].values:
            raise NameNotFoundError(f'\n"{disease_name}" did not find in database. \nPlease check your flag type (-m for miRNA, -d for disease) and enter a valid name.')
        return df[df['diseaseName'] == disease_name]
    return None

from tabulate import tabulate
# Browsing data base on input mirna/disease name
# --- miRNA
def check_mirna_in_database(df, query):
    """Browse the database for miRNAs that match the query."""
    matched_miRNAs = df[df['miRNA'].str.contains(query, case=False, na=False)]['miRNA'].unique()
    if matched_miRNAs.size == 0:
        raise MatchNotFoundError(f'\nNo miRNA matches found for the query "{query}" in the database. \nPlease check your browse type (mirna or disease) and enter a valid query.')
    else:
        print(f"    The browsing type is 'mirna' \n    The query you entered is '{query}'\n")
        print(f'Here are {matched_miRNAs.size} miRNA names that match your query:\n')
        return matched_miRNAs

# --- disease
def check_disease_in_database(df, query):
    """Browse the database for diseases that match the query."""
    matched_diseases = df[df['diseaseName'].str.contains(query, case=False, na=False)]['diseaseName'].unique()
    if matched_diseases.size == 0:
        raise MatchNotFoundError(f'\nNo disease matches found for the query "{query}" in the database. \nPlease check your browse type (mirna or disease) and enter a valid query.')
    else:
        print(f"    The browsing type is 'disease' \n    The query you entered is '{query}'\n")
        print(f'Here are {matched_diseases.size} miRNA names that match your query:\n')
        for disease in matched_diseases:
            print(f'{disease}')
    return None

#---------------------------------------------------------------------------------------------------------
# Defining executing functions

# Printing example usage
def print_example_usage():
    print('Example usage:')
    print('\nSearching by miRNA:')
    print(' - "python script-name.py -m hsa-miR-892c-5p"')
    print(' - "python script-name.py -m hsa-miR-892c-5p -ms 95"') 
    print(' - "python script-name.py -m hsa-miR-892c-5p -ms 95, -gs 0.9"')
    print('\nSearching by disease:')
    print(' - "python script-name.py -d obesity -ms 0.95"')
    print(' - "python script-name.py -d "hypercholesterolemia, autosomal recessive" -ms 95 -gs 0.95"')
    print('\nBrowsing query:')
    print(' - "python script-name.py -b mirna -q let-7"')
    print(' - "python script-name.py -b disease -q "type 1"')
    print('\n --> Now you can look up for the associated miRNAs / Genes/ Diseases of your query :)')

# Loading data
def load_data(file_path):
    """Load the CSV data into a pandas DataFrame."""
    return pd.read_csv(file_path)

# Filtering data based on mirna/disease and mirna scores/gene score
# --- miRNA
def search_by_mirna(df, mirna, mirna_score, gene_score):
    """Search for diseases and genes associated with a given miRNA."""
    mirna = mirna[0] if mirna else None
    filtered_df = df[(df['miRNA'] == mirna) & 
                     (df['miRNA_pred_score'] >= mirna_score) & 
                     (df['confidenceScore'] >= gene_score)]
    
    print(f'Matching diseases associated to the input miRNA when:\n   miRNA score >= {mirna_score}\n   gene_score >= {gene_score}\n')
    print(f'Here are the associated [Diseases] and [Genes] to the input [miRNA]: "{mirna}"\n')
    print(filtered_df[['miRNA', 'diseaseName', 'geneSymbol']].to_markdown())
    
# --- disease
def search_by_disease(df, disease, mirna_score, gene_score):
    """Search for miRNAs and genes associated with a given disease."""
    disease = disease[0] if disease else None
    filtered_df = df[(df['diseaseName'] == disease) & 
                     (df['miRNA_pred_score'] >= mirna_score) & 
                     (df['confidenceScore'] >= gene_score)]

    print(f'Matching miRNAs associated to the input disease where:\n   miRNA score >= {mirna_score}\n   gene_score >= {gene_score}\n')
    print(f'Here are the associated [miRNAs] and [Genes] to the input [Disease]: "{disease}"\n')
    print(filtered_df[['miRNA', 'diseaseName', 'geneSymbol']].to_markdown())

# Searching query: miRNA/disease name
def perform_search(df, args):
    if args.mirna:
        return search_by_mirna(df, args.mirna, args.mirna_score, args.gene_score)
    elif args.disease:
        return search_by_disease(df, args.disease, args.mirna_score, args.gene_score)

# Browsing query: miRNA/disease name
def perform_browse(df, args):
    if args.browse.lower() == 'mirna':
        return check_mirna_in_database(df, args.query)
    elif args.browse.lower() == 'disease':
        return check_disease_in_database(df, args.query)

#---------------------------------------------------------------------------------------------------------
# Defining main function
def main():
    args = parser.parse_args()
    
    # Loading data
    validate_file(args.file)
    df = load_data(args.file)
    
    # Executing the rest error trapping
    # --- Checking input miRNA/disease name numbers
    if args.mirna and args.disease:
        raise SearchConflictError('\nOnly one miRNA name or one disease name is allowed at a time. Please check your input.')
    if args.mirna and len(args.mirna) > 1:
        raise ValueError('\nOnly one miRNA name can be searched at a time. Please provide a single miRNA name.')
    if args.disease and len(args.disease) > 1:  
        raise ValueError('\nOnly one disease name can be searched at a time. Please provide a single disease name.')
    # --- Checking if the scores are in the acceptable range
    validate_scores(args.mirna_score, args.gene_score)
    # --- Checking if the -e flag is provided to print examples
    if args.example:
        print_example_usage()
        return
    # --- Checking if essential arguments are provided
    validate_names_and_scores(args.mirna, args.disease, args.mirna_score, args.gene_score)
    validate_browse_and_query(args.browse, args.query)
    # --- Checking if the miRNA/disease name exist in database
    check_mirna_name(df, args.mirna)
    check_disease_name(df, args.disease)

    # Performing search or browse based on arguments
    results = None  # initializes the 'results' variable to None
    if args.mirna or args.disease:
        results = perform_search(df, args) # store the search outcome to the 'results' variable 
        if results is not None:
            print(results)
        return                             
    elif args.browse and args.query:
        results = perform_browse(df, args) # store the search outcome to the 'results' variable 
        if results is not None:
            print(results)
        return
    if results is None:
        print("No valid search criteria provided. Use --help for more information.")
    

if __name__ == '__main__':
    main()
else:
	print("run as module\n")