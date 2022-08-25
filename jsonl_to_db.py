import jsonlines
import pandas as pd

import cryptography
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import JSON

# tqdm is for progress bar generation.
from tqdm import tqdm

# Establish special datatypes for certain columns 
dtype = {
    'head_templates': JSON,
    'etymology_templates': JSON,
    'sounds': JSON,
    'forms': JSON,
    'senses': JSON,
    'wikipedia': JSON,
    }

# Connect to the mysql database
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="user_name",
                               pw="password123",
                               db="database_name"))



# Script is slow, I need to find a way to make it faster.
# generators is a possible solution.
# consider using dict.keys() > yields a list of keys.

# Main parser function.
def parsefile(filename):
    with jsonlines.open("{}.jsonl".format(filename)) as reader:
        for pydict in tqdm(reader):
            
            # Check if the keys of the pydict dictionary exist.
            if 'pos' in pydict:
                pos = str(pydict['pos'])
            else:
                pos = ""
            if 'head_templates' in pydict:
                head_templates = str(pydict['head_templates'])
            else:
                head_templates = ""
            if 'etymology_text' in pydict:
                etymology_text = str(pydict['etymology_text'])
            else:
                etymology_text = ""
            if 'etymology_templates' in pydict:
                etymology_templates = str(pydict['etymology_templates'])
            else:
                etymology_templates = ""
            if 'sounds' in pydict:
                sounds = str(pydict['sounds'])
            else:
                sounds = ""
            if 'forms' in pydict:
                forms = str(pydict['forms'])
            else:
                forms = ""
            if 'word' in pydict:
                word = str(pydict['word'])
            else:
                word = ""
            if 'lang' in pydict:
                lang = str(pydict['lang'])
            else:
                lang = ""
            if 'lang_code' in pydict:
                lang_code = str(pydict['lang_code'])
            else:
                lang_code = ""
            if 'senses' in pydict:
                senses = str(pydict['senses'])
            else:
                senses = ""
            if 'wikipedia' in pydict:
                wikipedia = str(pydict['wikipedia'])
            else:
                wikipedia = ""

            # New Dictionary with the correct values and correct columns.
            data = {
                    'pos': [pos],
                    'head_templates': [head_templates],
                    'etymology_text': [etymology_text],
                    'etymology_templates': [etymology_templates],
                    'sounds' : [sounds],
                    'forms' : [forms],
                    'word': [word],
                    'lang': [lang],
                    'lang_code': [lang_code],
                    'senses' : [senses],
                    'wikipedia': [wikipedia],
                }

            df2 = pd.DataFrame(data)
            df2.to_sql("{}".format(filename), con = engine, if_exists = 'append', index=True, chunksize = 1000, method='multi', dtype=dtype)

"""
parsefile('determiners')
parsefile('abbreviations')
parsefile('adverbs')
parsefile('articles')
parsefile('conjunctions')
parsefile('particles')
parsefile('prepositions')
parsefile('pronouns')
parsefile('adjectives')
parsefile('nouns')
parsefile('verbs')
"""


import multiprocessing


if __name__ == "__main__":
    # creating processes
    p1 = multiprocessing.Process(target=parsefile, args=('articles',))
    p2 = multiprocessing.Process(target=parsefile, args=('particles',))
    p3 = multiprocessing.Process(target=parsefile, args=('abbreviations',))


    # start processes
    p1.start()
    p2.start()
    p3.start()

    # wait until processes are finished
    p1.join()
    p2.join()
    p3.join()

    print("Three jobs done !")


    p1 = multiprocessing.Process(target=parsefile, args=('determiners',))
    p2 = multiprocessing.Process(target=parsefile, args=('conjunctions',))
    p3 = multiprocessing.Process(target=parsefile, args=('pronouns',))
    p4 = multiprocessing.Process(target=parsefile, args=('prepositions',))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()

    print("Four jobs done !")

    p1 = multiprocessing.Process(target=parsefile, args=('adverbs',))
    p2 = multiprocessing.Process(target=parsefile, args=('adjectives',))
    p3 = multiprocessing.Process(target=parsefile, args=('verbs',))
    p4 = multiprocessing.Process(target=parsefile, args=('nouns',))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()

print("All done !")

