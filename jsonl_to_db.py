import pandas as pd    
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import JSON, TEXT, CHAR
from alive_progress import alive_it

# Enter your username and password to your SQL database. 
user="username"
pw="password"

# Connect to database
engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/")

# create a database called 'dictionary'
engine.execute("CREATE DATABASE dictionary")

# Connect to the dictionary database
engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/dictionary")

# These are the desired datatypes for the SQL tables
datatype = {
    'word': TEXT,
    'pos': TEXT,
    'senses': JSON,
    'forms': JSON,
    'synonyms': JSON,
    'antonyms':JSON,
    'hypernyms': JSON,
    'hyponyms': JSON,
    'sounds': JSON,
    'lang': CHAR(10),
    'lang_code': CHAR(3),
    'head_templates': JSON,
    'etymology_text': TEXT,
    'etymology_templates': JSON,
    'inflection_templates': JSON,
    'translations': JSON,
    'derived': JSON,
    'related': JSON,
    'wikipedia': JSON,
    'categories':JSON
    }

# Name of the files that are going to be parsed and sent to the database. 
items = [
    'articles',
    'particles',
    'abbreviations',
    'determiners',
    'conjunctions',
    'pronouns',
    'prepositions',
    'adverbs',
    'adjectives',
    'verbs',
    'nouns']

# Main function. Creates a dataframe object from the jsonl files and sends them to the database.
def export_to_db():
    for item in alive_it(items):
        df = pd.read_json(path_or_buf="{}.jsonl".format(item), lines=True)
        df = df.astype(str) 
        df.to_sql("{}".format(item), con = engine, if_exists = 'append', index=False, chunksize = 1000, method='multi',dtype=datatype)
        print("\n")

export_to_db()
