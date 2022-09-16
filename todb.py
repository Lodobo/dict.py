# Usage : 'python3 todb.py en fr es'

import pandas as pd    
from sqlalchemy import Table, Column, Index, create_engine, MetaData
from sqlalchemy.dialects.mysql import INTEGER, JSON, TEXT, CHAR
from sqlalchemy_utils import database_exists, create_database, drop_database
from alive_progress import alive_bar
import sys

filenames=('en','en_lexemes','fr','sv','ls','la','es','de','it','ru','fi','ar','nl','no','nb','nn','da','se','smj','smn','sms','ru','pt','pl','zh','ja','is','ur')
arglist = sys.argv
intersection = list(set(filenames) & set(arglist))

if len(sys.argv) == 1:
    print("\nError : expected at least one argument\n")
    print("Options : all, en, en_lexemes, fr, sv, ls, la, es, de, it, ru, fi, ar, nl, no, nb, nn, da, se, smj, smn, sms, ru, pt, pl, zh, ja, is, ur\n")
    quit()
elif len(intersection) == 0 and 'all' not in arglist:
    print("\nError : No valid argument\n")
    print("Options : all, en, en_lexemes, fr, sv, ls, la, es, de, it, ru, fi, ar, nl, no, nb, nn, da, se, smj, smn, sms, ru, pt, pl, zh, ja, is, ur\n")
    quit()

# Enter your username and password to your SQL database. 
user="username"
pw="password123"

engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/dictionary")

# Check if database already exists
if not database_exists(engine.url):
    create_database(engine.url)

def create_table(tablename):
    meta = MetaData()
    table = Table(
       f'{tablename}', meta, 
       Column('index', INTEGER, primary_key = True), 
       Column('word', CHAR(30, collation="utf8mb4_unicode_ci"), nullable=False),
       Column('pos', CHAR(15), nullable=False),
       Column('senses', JSON, nullable=False),
       Column('forms', JSON),
       Column('synonyms', JSON),
       Column('antonyms', JSON),
       Column('hypernyms', JSON),
       Column('hyponyms', JSON),
       Column('meronyms', JSON),
       Column('holonyms', JSON),
       Column('troponyms', JSON),
       Column('sounds', JSON),
       Column('lang', CHAR(20), nullable=False),
       Column('lang_code', CHAR(3), nullable=False),
       Column('head_templates', JSON),
       Column('etymology_text', TEXT(collation="utf8mb4_unicode_ci")),
       Column('etymology_templates', JSON),
       Column('inflection_templates', JSON),
       Column('coordinate_terms', JSON),
       Column('form_of', JSON),
       Column('translations', JSON),
       Column('source', JSON),
       Column('hyphenation', JSON),
       Column('proverbs', JSON),
       Column('instances', JSON),
       Column('abbreviations', JSON),
       Column('derived', JSON),
       Column('related', JSON),
       Column('wikipedia', JSON),
       Column('categories', JSON),
       Column('alt_of', JSON),
       Column('topics', JSON),   
    )
    Index('idx', table.c.index)
    Index('word_idx', table.c.word)
    Index('pos-idx', table.c.pos)
    Index('lang-idx', table.c.lang_code)
    meta.create_all(engine)

# Datatypes for the SQL tables
datatype = {
    'index': INTEGER,
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
    'lang': CHAR(20),
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
    'alt_of':JSON,
    'topics':JSON
    }

print("\nSending data to MySQL database...\n")

# Main function. Creates a dataframe object from the jsonl files and sends the data to the database.
def export_to_db(fn):

    create_table(fn)

    # Count total lines for progress bar generation
    with open(f"{fn}.jsonl", 'r') as fp:
        num_lines = sum(1 for line in fp)

    with alive_bar(num_lines, title=f"{fn}", title_length=13, spinner=None) as bar: 

        chunk = pd.read_json(path_or_buf=f"{fn}.jsonl", lines=True, chunksize=2000)
        for df in chunk:
            x = df.shape[0]
            indexNames = df[ df['word'].str.len() > 30].index
            df.drop(indexNames, inplace=True)
            df.to_sql(f"{fn}", con = engine, if_exists = 'append', index=False, chunksize = 2000, dtype=datatype)
            bar(x)

if 'all' in arglist:
    for file in filenames:
        export_to_db(file)
else:
    for file in intersection:
        export_to_db(file)

print("\nData has succesfully been sent to the database !")
