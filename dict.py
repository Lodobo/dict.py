#!/usr/bin/env python3

### https://github.com/Lodobo/TUI-Dictionary ###

### The script fetches dictionary data from a database and displays it in terminal ###

import argparse, json, random
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table
from rich.padding import Padding
from rich.text import Text

###### defining CLI arguments #
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--word",type=str,default=None, help="Search for word in dictionary")
parser.add_argument("-p", "--pos",type=str,default=None, help="Specify a specific part of speech to search in")
parser.add_argument("-l", "--language",type=str,default="en",help="Select language to search in (default: en)")
parser.add_argument("-e", "--examples", help="Show examples", default=False,action="store_true")
parser.add_argument("-E", "--etymology", help="Show the etymology of the word",default=False ,action="store_true")
parser.add_argument("-s", "--synonyms", help="Show synonyms and antonyms", default=False,action="store_true")
parser.add_argument("-r", "--random", help="Discover a random word", default=False,action="store_true")
args = parser.parse_args()
# defining CLI arguments ######

###### ERROR HANDLING # 
possible_langs = ('en','fr','sv','ls','es','de','it','ru','fi','ar','nl','no','nb','nn','da','se','ls','rs','ss','ru','pt','pl','zh','ja','is','ur')

if args.language not in possible_langs:
    print("\nError : not a valid language\n")
    quit()

possible_pos = (None,'abbrev','adj','adv','adv_phrase','affix','article','character','circumfix','conj','det','infix','interfix','name','noun','num','particle','phrase','postp','prefix','prep','prep_phrase','pron','proverb','punct','suffix','symbol','verb')


if args.pos not in possible_pos:
    print("\nError : not a valid part of speech\n")
    print("Options : abbrev, adj, adv, adv_phrase, affix, article, character, conj, det, name, noun, num, particle, phrase, postp, prep, prep_phrase, pron, verb\n")
    quit()

if args.word == None and args.random == False:
    print("\nError : Expected one argument : --random or --word\n")
    quit()
if args.word and args.random:
    print("\nError : Conflicting arguments\n")
    quit()
if args.random and args.pos:
    print("\nError : Conflicting arguments. Part of speech is random")
# ERROR HANDLING ######


# ROW COUNT FOR GENERATING RANDOM WORDS. 
# Feeding this into rand.int seems to sometimes generate integers that are bigger than expected.
"""
row_counts = {
    'en':1158999,
    'en_lexemes':645944,
    'fr':385127,
    'sv':138190,
    'ls':966,
    'la':860994,
    'es':726291,
    'de':321953,
    'it':610398,
    'ru':424502,
    'fi':229875,
    'ar':127297,
    'nl':128689,
    'no':1778,
    'nb':72748,
    'nn':59385,
    'da':47233,
    'se':5446,
    'smj':966,
    'smn':570,
    'sms':616,
    'ru':424502,
    'pt':307671,
    'pl':128261,
    'zh':163317,
    'ja':134965,
    'is':22839,
    'ur':5050}
"""

###### DECIDING WHAT DATA TO REQUEST #
if args.random:
    randrow = random.randint(1, 645944)
    data = f"SELECT * FROM `en_lexemes` where `index`='{randrow}'"
elif args.pos:
    data = f"SELECT * FROM `{args.language}` WHERE word='{args.word}' and pos='{args.pos}'"
else:
    data = f"SELECT * FROM `{args.language}` WHERE word='{args.word}'"
# DECIDING WHAT DATA TO REQUEST ######

# Database connection info. Insert your database credentials.
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/dictionary"
                        .format(user="username",pw="password123"))

# Fetch data from database and store it in a dataframe.
df = pd.read_sql(data, con=engine)
df = df.sort_values(by=['pos'])
df = df.replace('null', np.nan)
# df.dropna(how='all', axis=1, inplace=True) # uncomment if you want to drop empty columns, might break something.

# Decide what word to display in case of a random request.
if args.random:
    WORD = df['word'].tolist()[0]
else:
    WORD = args.word

keys = df.columns.values.tolist()
word = df['word']
pos = df['pos']
senses = df['senses']
sounds = df['sounds']
etymology = df['etymology_text']

console = Console()

if len(df.index) == 0:
    print('\n404: Word not found in dictionary\n')

###### print functions #
def print_sounds(idx):
    """Print phonemic transcriptions of pronunciation to console"""
    if pd.isnull(sounds[idx]) == False:
        ls = json.loads(sounds[idx])
        for item in ls:
            if 'tags' in item and 'ipa' in item:
                # console.print(f"[bold]IPA[/bold] : [bright_cyan]{item['ipa']}[/bright_cyan] [grey70]({item['tags'][0]})[/grey70]")
                console.print(f"[bold]IPA[/bold] : [bright_cyan]{item['ipa']:<20}[/bright_cyan] [grey70]({item['tags'][0]})[/grey70]")
            elif 'ipa' in item:
                console.print(f"[bold]IPA[/bold] : [bright_cyan]{item['ipa']}[/bright_cyan]")
def print_etymology(idx):
    """Print Etymology to console"""
    if pd.isnull(etymology[idx]) == False:
        console.print("\n[bold][underline]Etymology[/underline] :\n")
        # print("  ", word[idx],f"({pos[idx]})")
        ety = etymology[idx]
        ety = Text(ety, overflow='crop')
        ety.stylize("grey70")
        ety = Padding(ety, (0,3))
        table = Table(show_lines=False, box=None, show_header=False, padding=(0, 0, 1, 0), pad_edge=False)
        table.add_column("etymology", justify="full", no_wrap=False,  max_width=94)
        table.add_row(ety)
        console.print(table)
def print_definitions(idx):
    """Print Definitions to console"""
    console.print("\n[bold][underline]Definitions[/underline] : \n")
    ls = json.loads(senses[idx])
    table = Table(show_lines=False, box=None, show_header=False, padding=(0, 0, 1, 0), pad_edge=False)

    table.add_column("n", justify='centre',no_wrap=True)
    table.add_column("Definition", justify="full", no_wrap=False,  max_width=82)

    for count, dct in enumerate(ls):
        if 'glosses' in dct:
            glosses = dct['glosses']
            glosses = " > ".join(glosses)
            glosses = Text(f"{glosses}", overflow="fold", justify='full')
            # glosses.stylize(justify='full', )
            # text.stylize("bold magenta", 0, 6)
            num = Text(f"{count}.")
            num = Padding(num, (0,3))
            table.add_row(num,glosses)

        if args.examples and 'examples' in dct:
            example = f"Ex: {dct['examples'][0]['text']}"
            example = Text(example)
            example.stylize("grey70")
            # example = Padding(example, (0,3))
            # console.print(example)
            table.add_row("",example)
    console.print(table)
    print()

def print_synonyms(idx):
    """Print synonyms, antonyms, hypernyms, hyponyms, meronyms, troponyms and holonyms to console"""
    if 'synonyms' in keys and pd.isnull(df['synonyms'][idx]) == False:
        console.print("\n[bold][underline]Synonyms[/underline] :\n")
        ls = json.loads(df['synonyms'][idx])
        for item in ls:
            word = ""
            tags = ""
            english = ""        
            if 'word' in item:
                word = item['word']
            if 'tags' in item:
                tags = item['tags']
                tags = " / ".join(tags)
                tags = f"({tags})"
            print(f"   {word:<20} {tags}")
            # print("   ",word,"\t\t", tags)
    if 'antonyms' in keys  and pd.isnull(df['antonyms'][idx]) == False:
        console.print("\n[bold][underline]Antonyms[/underline] :\n")
        ls = json.loads(df['antonyms'][idx])
        for item in ls:
            word = ""
            tags = ""
            english = ""        
            if 'word' in item:
                word = item['word']
            if 'tags' in item:
                tags = item['tags']
                tags = " / ".join(tags)
                tags = f"({tags})"
            print(f"   {word:<20} {tags}")
    if 'hypernyms' in keys and pd.isnull(df['hypernyms'][idx]) == False:
        console.print("\n[bold][underline]Hypernyms[/underline] :\n")
        ls = json.loads(df['hypernyms'][idx])
        for item in ls:
            word = ""
            tags = ""
            english = ""        
            if 'word' in item:
                word = item['word']
            if 'tags' in item:
                tags = item['tags']
                tags = " / ".join(tags)
                tags = f"({tags})"
            print(f"   {word:<20} {tags}")
    if 'hyponyms' in keys and pd.isnull(df['hyponyms'][idx]) == False:
        console.print("\n[bold][underline]Hyponyms[/underline] :\n")
        ls = json.loads(df['hyponyms'][idx])
        for item in ls:
            word = ""
            tags = ""
            english = ""        
            if 'word' in item:
                word = item['word']
            if 'tags' in item:
                tags = item['tags']
                tags = " / ".join(tags)
                tags = f"({tags})"
            print(f"   {word:<20} {tags}")
    if 'meronyms' in keys and pd.isnull(df['meronyms'][idx]) == False:
        console.print("\n[bold][underline]meronyms[/underline] :\n")
        ls = json.loads(df['meronyms'][idx])
        for item in ls:
            word = ""
            tags = ""
            english = ""        
            if 'word' in item:
                word = item['word']
            if 'tags' in item:
                tags = item['tags']
                tags = " / ".join(tags)
                tags = f"({tags})"
            print(f"   {word:<20} {tags}")
    if 'troponyms' in keys and pd.isnull(df['troponyms'][idx]) == False:
        console.print("\n[bold][underline]Troponyms[/underline] :\n")
        ls = json.loads(df['troponyms'][idx])
        for item in ls:
            word = ""
            tags = ""
            english = ""        
            if 'word' in item:
                word = item['word']
            if 'tags' in item:
                tags = item['tags']
                tags = " / ".join(tags)
                tags = f"({tags})"
            print(f"   {word:<20} {tags}")
    if 'holonyms' in keys and pd.isnull(df['holonyms'][idx]) == False:
        console.print("\n[bold][underline]Holonyms[/underline] :\n")
        ls = json.loads(df['holonyms'][idx])
        for item in ls:
            word = ""
            tags = ""
            english = ""        
            if 'word' in item:
                word = item['word']
            if 'tags' in item:
                tags = item['tags']
                tags = " / ".join(tags)
                tags = f"({tags})"
            print(f"   {word:<20} {tags}")
# print functions ######

###### execute #
if args.synonyms:
    for index, row in df.iterrows():
        print()
        POS = pos[index]
        POS = POS.upper()
        p1 = Panel(f"[bold]{WORD}", expand=False)
        p2 =  Panel(f"[bold]{POS}", expand=False)
        console.print(Columns([p2, p1]))
        print_synonyms(index)
        print()
        quit()

for index, row in df.iterrows():
    print()
    POS = pos[index]
    POS = POS.upper()
    p1 = Panel(f"[bold]{WORD}", expand=False)
    p2 =  Panel(f"[bold]{POS}", expand=False)

    console.print(Columns([p2, p1]))

    print_sounds(index)
    if args.etymology:
        print_etymology(index)
    print_definitions(index)
# execute ######


