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
    'word': TEXT,
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

# Name of the files that are going to be parsed and sent to the database. 
items = ['articles','particles','abbreviations','determiners','conjunctions','pronouns','prepositions','adverbs','adjectives','verbs','nouns']


# Main function. Creates a dataframe object from the jsonl files and sends them to the database.
def export_to_db(fn):
        df = pd.read_json(path_or_buf="{}.jsonl".format(fn), lines=True)
        df.to_sql("{}".format(fn), con = engine, if_exists = 'replace', index=False, chunksize = 1000, method='multi',dtype=datatype)

def change_type(table):
    
    # Delete long words
    engine.execute("DELETE FROM {} WHERE LENGTH(word) > 30".format(table))
    
    # Alter datatypes
    engine.execute(" ALTER TABLE {} MODIFY COLUMN word char(30)".format(table))


for pos in alive_it(items):
    export_to_db(pos)
    change_type(pos)


engine.execute(" ALTER TABLE abbreviations MODIFY COLUMN word char(20)")
engine.execute(" ALTER TABLE particles MODIFY COLUMN word char(10)")
engine.execute(" ALTER TABLE articles MODIFY COLUMN word char(10)")

print("All done !")
