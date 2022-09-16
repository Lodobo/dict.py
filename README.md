# TUI-Dictionary

!screenshot.png(https://github.com/Lodobo/TUI-Dictionary/blob/main/screenshot.png?raw=true)

## Description

This repository has four scripts. `downloader.sh` is a bash script that downloads wiktionary entries from kaikki.org with `wget`. `todb.py` is a python script that parses the downloaded jsonl files and sends the information to a database. `downloadAndSendToDB.sh` is a bash script that downloads AND runs the todb.py script. Finally, `TDict.py` is a TUI dictionary implementation of the database.

To quickly set up the database, it is possible to directly download a sql file. Just do the following :
1) Install mysql
2) Download .sql file(s):
    - For the english dictionary: `$ wget https://www.dropbox.com/s/mgb1982eo8u6850/en.zip`
    - For extra languages (option): `$ wget https://www.dropbox.com/s/za14slf0hqfk2yl/extra-languages.zip`
3) Unzip file(s):
    - `$ unzip en.zip`
    - `$ unzip extra-languages.zip`
4) Launch mysql and create account
5) Create database:
    - `mysql> CREATE DATABASE dictionary;`
6) Import tables to database:
    - `$ mysql –u username –p dictionary < en.sql`
    - And any optional languages: `$ mysql –u username –p dictionary < french.sql`
 
Warning: the jsonl files will consume a bit over 1gb of storage.

## Dependencies:

- pandas
- cryptography
- sqlalchemy
- pymysql
- mysql
- rich
- alive_progress
- wget

## Using TDict.py

|options|Description|
|----|----|
|-h, --help|Show a help mesage|
|-w [WORD], --word [WORD]|Search for given word in dictionary|
|-p [part of speech], --pos [part of speech]|Specify a specific part of speech to search in|
|-l [lang], --language [lang]|Select language to search in|
|-e, --examples|Show examples|
|-E, --etymology|Show the etymology of the word|
|-s, --synonyms|Show the synonyms and antonyms of the word|

## How to fetch underlying JSON objects in SQL:
```sql
-- Definitions
SELECT sn.raw_glosses, sn.glosses FROM verbs, JSON_TABLE(verbs.senses, '$[*]'
COLUMNS (
    `glosses` TEXT PATH '$.glosses[*]',
    `raw_glosses` TEXT PATH '$.raw_glosses[*]')
    ) sn where word='see';
```
```sql
-- Synonyms
SELECT syn.word, syn.sense FROM verbs, JSON_TABLE(verbs.synonyms, '$[*]'
COLUMNS (
    `word` TEXT PATH '$.word',
    `sense` TEXT PATH '$.sense')
    ) syn where verbs.word='see';
```
```sql
-- Forms
SELECT fm.form, fm.tags FROM verbs, JSON_TABLE(verbs.forms, '$[*]'
COLUMNS (
    `form` TEXT PATH '$.form',
    `tags` JSON PATH '$.tags')
    ) fm where verbs.word='see';
```
```sql
-- Pronunciation
SELECT pr.ipa  FROM verbs, JSON_TABLE(verbs.sounds, '$[0]'
COLUMNS (
    `ipa` TEXT PATH '$.ipa')
    ) pr where verbs.word='see';
```
