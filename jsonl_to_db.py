import pandas as pd    
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import JSON, TEXT, CHAR
from alive_progress import alive_it

# Enter your username and password to your SQL database. 
user="username"
pw="password123"

# Connect to database
engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/")

# create a database called 'dictionary'
engine.execute("CREATE DATABASE dictionary")

# Connect to the dictionary database
engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/dictionary")

# These are the desired datatypes for the SQL tables
datatype = {
    'word': CHAR(30),
    'pos': CHAR(10),
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
    'etymology_text': TEXT,
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
    'categories':JSON
    }

# Main function. Creates a dataframe object from the jsonl files and sends them to the database.
def export_to_db(fn):
        
        # Read file
        df = pd.read_json(path_or_buf="{}.jsonl".format(fn), lines=True)
        
        # Delete rows if words are too long.
        indexNames = df[ df['word'].str.len() > 30].index 
        df.drop(indexNames, inplace=True)
        
        # Send to mysql database
        df.to_sql("{}".format(fn), con = engine, if_exists = 'replace', index=False, chunksize = 1000, method='multi',dtype=datatype)


# Name of the files that are going to be parsed and sent to the database. 
items = ['articles','particles','abbreviations','determiners','conjunctions','pronouns','prepositions','adverbs','adjectives','verbs','nouns']

for pos in alive_it(items):
    export_to_db(pos)

print("All done !")
