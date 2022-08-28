import jsonlines
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import JSON, TEXT

# tqdm is for progress bar generation.
from tqdm import tqdm

# Establish special datatypes for certain columns 

dtype = {
    'head_templates': JSON,
    'etymology_text': TEXT,
    'etymology_templates': JSON,
    'inflection_templates': JSON,
    'sounds': JSON,
    'forms': JSON,
    'senses': JSON,
    'translations': JSON,
    'synonyms': JSON,
    'hypernyms': JSON,
    'hyponyms' : JSON,
    'antonyms':JSON,
    'derived' : JSON,
    'related': JSON,
    'wikipedia': JSON,
    'categories':JSON
    }

# Connect to the mysql database
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="user_name",
                               pw="password123",
                               db="database_name"))

# Main parser function.
def parsefile(filename):
    with jsonlines.open("{}.jsonl".format(filename)) as reader:
        for pydict in tqdm(reader):
            # Default fields
            fields = {'pos':[],'head_templates':[],'etymology_text':[],'etymology_templates':[],'inflection_templates':[],'sounds':[],'forms':[],'word':[],'synonyms':[],'hypernyms':[],'hyponyms':[],'antonyms':[],'derived':[],'related':[],'lang':[],'lang_code':[],'senses':[],'translations':[],'wikipedia':[],'categories':[]}
            
            # Convert the values of pydict into strings, for dataframe compatibility reasons
            keys = pydict.keys()
            values = pydict.values()
            values = [str(x) for x in values]
            newDict = { k:v for (k,v) in zip(keys, values)}
            
            # Create and merge dataframes with all fields
            df1 = pd.DataFrame.from_dict([newDict])
            df2 = pd.DataFrame(fields)
            df3 = df1.merge(df2, how='right')
            
            # Convert and send dataframe object to sql database
            df3.to_sql("{}".format(filename), con = engine, if_exists = 'append', index=False, chunksize = 1000, method='multi', dtype=dtype)

parsefile('articles')
parsefile('particles')
parsefile('abbreviations')
parsefile('determiners')
parsefile('conjunctions')

# parsefile('pronouns')
# parsefile('prepositions')
# parsefile('adverbs')
# parsefile('adjectives')
# parsefile('verbs')
# parsefile('nouns')

import multiprocessing

if __name__ == "__main__":
    # creating processes
    
    p1 = multiprocessing.Process(target=parsefile, args=('pronouns',))
    p2 = multiprocessing.Process(target=parsefile, args=('prepositions',))
    p3 = multiprocessing.Process(target=parsefile, args=('adverbs',))

    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()

    print("Three jobs done !")

    p1 = multiprocessing.Process(target=parsefile, args=('adjectives',))
    p2 = multiprocessing.Process(target=parsefile, args=('verbs',))
    p3 = multiprocessing.Process(target=parsefile, args=('nouns',))

    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()

print("All done !")
