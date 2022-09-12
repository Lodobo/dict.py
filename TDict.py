# Usage : 'python3 todb.py -l en'

import pandas as pd    
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import JSON, TEXT, CHAR
from sqlalchemy_utils import database_exists, create_database
from alive_progress import alive_bar

import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--language", type=str, help="Select language.")    
args = parser.parse_args()

# Enter your username and password to your SQL database. 
user="username"
pw="password"

engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/dictionary")

# Check if database already exists
if not database_exists(engine.url):
    create_database(engine.url)

# Datatypes for the SQL tables
datatype = {
    'word': CHAR(30, collation="utf8mb4_unicode_ci"),
    'pos': CHAR(15),
    'senses': JSON,
    'forms': JSON,
    'synonyms': JSON,
    'antonyms':JSON,
    'hypernyms': JSON,
    'hyponyms': JSON,
    'meronyms': JSON,
    'troponyms':JSON,
    'holonyms': JSON,
    'sounds': JSON,
    'lang': CHAR(10),
    'lang_code': CHAR(3),
    'head_templates': JSON,
    'etymology_text': TEXT(collation="utf8mb4_unicode_ci"),
    'etymology_templates': JSON,
    'inflection_templates': JSON,
    'coordinate_terms': JSON,
    'form_of': JSON,
    'translations': JSON,
    'source': JSON,
    'hyphenation': JSON,
    'proverbs': JSON,
    'instances': JSON,
    'abbreviations': JSON,
    'derived': JSON,
    'related': JSON,
    'wikipedia': JSON,
    'categories':JSON,
    'topics':JSON
    }

print("\nSending data to MySQL database")

# Main function. Creates a dataframe object from the jsonl files and sends the data to the database.
def export_to_db(fn):

    pwd = os.getcwd()

    # Count total lines for progress bar generation
    with open(f"{fn}.jsonl", 'r') as fp:
        num_lines = sum(1 for line in fp)

    df1 = pd.DataFrame(columns=['word','pos','senses','forms','synonyms','antonyms','hypernyms','hyponyms','meronyms','troponyms','holonyms','sounds','lang','lang_code','head_templates','etymology_text','etymology_templates','inflection_templates','coordinate_terms','form_of','translations','source','hyphenation','proverbs','instances','abbreviations','derived','related','wikipedia','categories','topics'])

    with alive_bar(num_lines, title=f"{fn}", title_length=13, spinner=None) as bar: 

        chunk = pd.read_json(path_or_buf=f"{fn}.jsonl", lines=True, chunksize=2000)
        for df2 in chunk:
            df = pd.concat([df1, df2])
            x = df.shape[0]

            indexNames = df[ df['word'].str.len() > 30].index
            df.drop(indexNames, inplace=True)
            df.to_sql(f"{fn}", con = engine, if_exists = 'append', index=False, chunksize = 2000, dtype=datatype)
            bar(x)
    
    # create index on table for faster read speeds
    engine.execute(f"CREATE INDEX `idx` ON {fn} (word)")

items = ['en_articles','en_particles','en_determiners','en_conjunctions','en_prepositions','en_pronouns','en_abbreviations','en_adverbs','en_adjectives','en_verbs','en_nouns','en']
# valid language options: ['en', 'fr', 'sv', 'la', 'es', 'de', 'it', 'ru','fi','ar','nl','no','da','se']


# Execute the function
if args.language == 'en':

    for item in items:
        export_to_db(item)
else:
    export_to_db(f'{args.language}')

print("\nData has succesfully been sent to the database !")



