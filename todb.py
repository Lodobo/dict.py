import pandas as pd    
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import JSON, TEXT, CHAR
from alive_progress import alive_bar


# Enter your username and password to your SQL database. 
user="username"
pw="password123"

# Connect to database
engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/")

# Create a database called dictionary
engine.execute("CREATE DATABASE dictionary")

# Connection to the dictionary database
engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/dictionary")

# Desired datatypes for the SQL tables
datatype = {
    'word': CHAR(30),
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
    'categories':JSON,
    'topics':JSON
    }

# Main function. Creates a dataframe object from the jsonl files and sends the data to the database.
def export_to_db(fn):

    # Count total lines for progress bar generation
    with open(f"{fn}.jsonl", 'r') as fp:
        num_lines = sum(1 for line in fp)

    df1 = pd.DataFrame(columns=['word','pos','senses','forms','synonyms','antonyms','hypernyms','hyponyms','meronyms','troponyms','holonyms','sounds','lang','lang_code','head_templates','etymology_text','etymology_templates','inflection_templates','coordinate_terms','form_of','translations','source','hyphenation','proverbs','instances','abbreviations','derived','related','wikipedia','categories','topics'])

    with alive_bar(num_lines, title=f"{fn}", title_length=13, spinner=None) as bar: 

        chunk = pd.read_json(path_or_buf="{}.jsonl".format(fn), lines=True, chunksize=2000)
        for df2 in chunk:
            df = pd.concat([df1, df2])
            x = df.shape[0]

            indexNames = df[ df['word'].str.len() > 30].index
            df.drop(indexNames, inplace=True)
            df.to_sql(f"{fn}", con = engine, if_exists = 'append', index=False, chunksize = 2000, dtype=datatype)
            bar(x)
    
    # create index on table for faster read speeds
    engine.execute(f"CREATE INDEX `idx` ON {fn} (word)")

# Name of the files that are going to be parsed and sent to the database. 
items = ['articles','particles','determiners','conjunctions','prepositions','pronouns','abbreviations','adverbs','adjectives','verbs','nouns','all_words']

for item in items:
    export_to_db(item)

print("\nAll done !")



