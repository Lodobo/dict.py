# CLI-Dictionary

![screenshot.jpg](https://raw.githubusercontent.com/Lodobo/TUI-Dictionary/main/screenshot.jpg)

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
 
Warning: the en.sql file is 400mb in size in compressed format and 3.2 gb when uncompressed. The extra-languages.sql file is 680mb in size in compressed format and 7.9 gb when uncompressed. The database itself occupies more space than the .sql files. The tables for the english dictionary take up 5.6gb.

## Dependencies:

- pandas
- cryptography
- sqlalchemy
- pymysql
- mysql
- rich
- alive_progress
- wget

**To install pip dependencies**:
`pip install -r requirements.txt`
or:
`python3 -m pip install -r requirements.txt`

## Using TDict.py

|options|Description|
|----|----|
|-h, --help|show a help mesage|
|-w [WORD], --word [WORD]|search for given word in dictionary|
|-p [part of speech], --pos [part of speech]|specify a specific part of speech to search in|
|-l [lang], --language [lang]|select language to search in|
|-e, --examples|show examples|
|-E, --etymology|show the etymology of the word|
|-s, --synonyms|show the synonyms and antonyms of the word|
|-r, --random|search a random word in the dictionary|

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
