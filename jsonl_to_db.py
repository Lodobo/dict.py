import jsonlines
import pandas as pd

import cryptography
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import JSON

from tqdm import tqdm
from time import sleep

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

# Main parser function.
def parsefile(filename):
    with jsonlines.open("{}.jsonl".format(filename)) as reader:
        for pydict in tqdm(reader):
            
            # Check if the keys of the pydict dictionary exist.
            try:
                pos = str(pydict['pos'])
            except:
                Print("part of speech information is missing")
                raise(Warning)
            try:
                head_templates = str(pydict['head_templates'])
            except:
                head_templates = ""
            try:
                etymology_text = str(pydict['etymology_text'])
            except:
                etymology_text = ""
            try:
                etymology_templates = str(pydict['etymology_templates'])
            except:
                etymology_templates = ""
            try:
                sounds = str(pydict['sounds'])
            except:
                sounds = ""
            try:
                forms = str(pydict['forms'])
            except:
                forms = ""
            try:
                word = str(pydict['word'])
            except:
                word = ""
            try:
                lang = str(pydict['lang'])
            except:
                lang = ""
            try:
                lang_code = str(pydict['lang_code'])
            except:
                lang_code = ""
            try:
                senses = str(pydict['senses'])
            except:
                senses = ""
            try:
                wikipedia = str(pydict['wikipedia'])
            except:
                wikipedia = ""

            # Mew Dictionary of each column key.
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


parsefile('part_of_speech')

