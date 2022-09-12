#!/usr/bin/env python3

import argparse, json
import pandas as pd    

from sqlalchemy import create_engine, text
from rich.console import Console
from rich.panel import Panel
from rich.padding import Padding
from rich.text import Text

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--word", type=str,default="None",help="Search for word in dictionary")
parser.add_argument("-p", "--pos", type=str,default="all",help="Specify a specific part of speech to search in")
parser.add_argument("-l", "--language",nargs='?',type=str,default="en",help="Select language to search in (default: en)")
parser.add_argument("-e", "--examples", help="Show examples", action="store_true")
parser.add_argument("-E", "--etymology", help="Show the etymology of the word", action="store_true")
parser.add_argument("-s", "--synonyms", help="Show synonyms and antonyms", action="store_true")


args = parser.parse_args()

if args.word == "None":
    print("\nError : Expected one argument. \nRun 'Tdict -h' for help\n")
    quit()

if args.pos != "all" and args.language != "en":
    print("It isn't possible to search in specific parts of speech for languages other than english")

pos = args.pos.lower()

if args.language == "en":
    if pos == "all":
        table="en"
    elif pos in ('nouns','noun'):
        table="en_nouns"
    elif pos in ('verbs','verb','vb'):
        table="en_verbs"
    elif pos in ('adjectives', 'adjective', 'adj'):
        table="en_adjectives"
    elif pos in ('adverbs','adverb','adv'):
        table="en_adverbs"
    elif pos in ('abbreviations', 'abbreviation','abbr', 'abbrev'):
        table="en_abbreviations"
    elif pos in ('articles', 'article','art'):
        table="en_articles"
    elif pos in ('conjunctions','conjunction','conj'):
        table="en_conjunctions"
    elif pos in ('determiners','determiner','det'):
        table="en_determiners"
    elif pos in ('particles','particle','part'):
        table="en_particles"
    elif pos in ('prepositions','preposition','prep'):
        table="en_prepositions"
    elif pos in ('pronouns','pronoun','pron'):
        table="en_pronouns"
    else:
        print('Value error : Invalid part of speech')
        quit()
elif args.language == "sv":
    table="sv"
elif args.language == "fr":
    table="fr"

user="username"
pw="password123"

engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/dictionary")

data = f"SELECT * FROM {table} WHERE word='{args.word}'"

df = pd.read_sql(data, con=engine)
df = df.sort_values(by=['pos'])

def printsynonyms():
    print("    ",end="")
    print(i['word'], end="\t")
    if 'tags' in i:
        tags = i['tags']
        tags = " / ".join(tags)
        tags = f"({tags})"
        print(tags)
    else:
        print()


if len(df.index) > 0:
    console = Console()
    console.print(Panel(Text(f"{args.word}".upper(), justify="center", style="bold white")))
else:
    print('\n404: Word not found in dictionary\n')

for index, row in df.iterrows():
    pos = row['pos']
    pos = pos.upper()

    if pos == "INTJ":
        pos = "INTERJECTION"

    if args.etymology == True:
        if 'etymology_text' in row and row['etymology_text'] != 'null':
            etymology = Text(row['etymology_text'])
            etymology = Padding(etymology, (0,4))
            console.print("\n[bold white][underline]Etymology[/underline] : \n")
            console.print(etymology)
            quit()

    if args.synonyms == True:
        if 'synonyms' in row and row['synonyms'] != 'null':
            tmp = json.loads(row['synonyms'])
            console.print("\n[bold white][underline]Synonyms[/underline] : \n")
            for i in tmp:
                printsynonyms()
        elif 'antonyms' in row and row['antonyms'] != 'null':
            tmp = json.loads(row['antonyms'])
            console.print("\n[bold white][underline]Antonyms[/underline] : \n")
            for i in tmp:
                printsynonyms()
        elif 'hypernyms' in row and row['hypernyms'] != 'null':
            tmp = json.loads(row['hypernyms'])
            console.print("\n[bold white][underline]Hypernyms[/underline] : \n")
            for i in tmp:
                printsynonyms()
        elif 'hyponyms' in row and row['hyponyms'] != 'null':
            tmp = json.loads(row['hyponyms'])
            console.print("\n[bold white][underline]Hyponyms[/underline] : \n")
            for i in tmp:
                printsynonyms()
        elif 'meronyms' in row and row['meronyms'] != 'null':
            tmp = json.loads(row['meronyms'])
            console.print("\n[bold white][underline]Meronyms[/underline] : \n")
            for i in tmp:
                printsynonyms()
        elif 'holonyms' in row and row['holonyms'] != 'null':
            tmp = json.loads(row['holonyms'])
            console.print("\n[bold white][underline]holonyms[/underline] : \n")
            for i in tmp:
                printsynonyms()
        elif 'troponyms' in row and row['troponyms'] != 'null':
            tmp = json.loads(row['troponyms'])
            console.print("\n[bold white][underline]Troponyms[/underline] : \n")
            for i in tmp:
                printsynonyms()
        else:
            print("\n  No synonyms found in dictionary")
        print()
        quit()

    if 'sounds' in row and row['sounds'] != 'null':
        console.print(Panel(f"[bold white] {pos}", width=6 + len(pos)))

        tmp = json.loads(row['sounds'])
        for i in tmp:
            if 'tags' in i and 'ipa' in i:
                console.print(f"[bold]{i['tags'][0]}[/bold] : [bright_cyan]{i['ipa']}", end="\n")
            elif 'ipa' in i and i['ipa'] != "":
                console.print(f"[bold]IPA[/bold] : [bright_cyan]{i['ipa']}")

        tmp = json.loads(row['senses'])

        console.print("\n[bold][underline]Definitions[/underline] : \n")
        for count, i in enumerate(tmp, start=1):
            if 'glosses' in i:
                glosses = i['glosses']
                glosses = " > ".join(glosses)
                glosses = Text(f"{count}. {glosses}\n")
                glosses = Padding(glosses, (0,2))
                console.print(glosses)

                if args.examples and 'examples' in i:
                    example = f"Ex: {i['examples'][0]['text']}\n"
                    example = example
                    example = Text(example)
                    example.stylize("grey70")
                    example = Padding(example, (0,5))
                    console.print(example)
print()
