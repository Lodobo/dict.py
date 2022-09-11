#!/usr/bin/env python3

import pandas as pd    
from sqlalchemy import create_engine
from sqlalchemy import text
from rich.console import Console
from rich.panel import Panel
from rich.padding import Padding
from rich.text import Text

import argparse
import json


user="admin"
pw="euthymia"
engine = create_engine(f"mysql+pymysql://{user}:{pw}@localhost/dictionary")

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--word", type=str, help="Search for word in dictionary")
parser.add_argument("-p", "--pos", type=str, help="Specify a specific part of speech to search in")
parser.add_argument("-e", "--examples", help="Show examples", action="store_true")
args = parser.parse_args()



if args.word:
    pass
else:
    print("\nError : No input\n")
    quit()

items = ['articles','particles','determiners','conjunctions','prepositions','pronouns','abbreviations','adverbs','adjectives','verbs','nouns']

if args.pos in items:
    data = f"SELECT * FROM {args.pos} WHERE word='{args.word}'"

elif args.pos == None: 
    data = f"SELECT * FROM all_words WHERE word='{args.word}'"
else:
    print("\nError : Incorrect pos\n")
    print("You can search in the following parts of speech :\n")
    print("articles, particles, determiners, conjunctions, prepositions, pronouns,\nabbreviations, adverbs, adjectives, verbs, nouns")
    quit()

df = pd.read_sql(data, con=engine)
df = df.sort_values(by=['pos'])

console = Console()

console.rule(f"[bold white]"+f"{args.word}".upper())

for index, row in df.iterrows():
    pos = row['pos']
    pos = pos.upper()

    if pos == "INTJ":
        pos = "INTERJECTION"

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
            glosses = i['glosses']
            glosses = " > ".join(glosses)
            console.print(f"{count}. {glosses}\n")

            if args.examples and 'examples' in i:
                example = f"Ex: {i['examples'][0]['text']}\n"
                example = example
                example = Text(example)
                example.stylize("grey70")
                example = Padding(example, (0,2))
                console.print(example)


