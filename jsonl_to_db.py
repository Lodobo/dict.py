import pandas as pd    
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import JSON, TEXT, CHAR
from alive_progress import alive_bar

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
    
    # Count lines for progress bar generation
    with open(f"{fn}.jsonl", 'r') as fp:
        num_lines = sum(1 for line in fp)
                
    with alive_bar(num_lines, title=f"{fn}", title_length=13, spinner=None) as bar: 
        chunk = pd.read_json(path_or_buf="{}.jsonl".format(fn), lines=True, chunksize=500)
        df1 = pd.DataFrame(columns=['word','pos','senses','forms','synonyms','antonyms','hypernyms','hyponyms','meronyms','troponyms','holonyms','sounds','lang','lang_code','head_templates','etymology_text','etymology_templates','inflection_templates','coordinate_terms','form_of','translations','source','hyphenation','proverbs','instances','abbreviations','derived','related','wikipedia','categories'])
        for df2 in chunk:
            df = pd.concat([df1, df2])
            x = df.shape[0]

            indexNames = df[ df['word'].str.len() > 30].index
            df.drop(indexNames, inplace=True)
            df.to_sql(f"{fn}", con = engine, if_exists = 'append', index=False, chunksize = 500, dtype=datatype)

            bar(x)


# Name of the files that are going to be parsed and sent to the database. 
items = ['articles','particles','abbreviations','determiners','conjunctions','pronouns','prepositions','adverbs','adjectives','verbs','nouns']

for pos in alive_it(items):
    export_to_db(pos)

print("All done !")
