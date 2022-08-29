# wiktionary-to-mysql

## Description

This repository has two scripts. First, a bash script that downloads wiktionary entries from kaikki.org with wget to a .jsonl file. Second, a python script that parses the jsonl files and sends the information to a database.

Each jsonl file corresponds to a part of speech (e.g. nouns). The script will create a table for each part of speech.

Warning: the jsonl files will consume a bit over 1gb of storage.

## Dependencies:

- wget
- pandas
- cryptography
- sqlalchemy
- alive_progress
- pymysql
- mysql
