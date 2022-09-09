# wiktionary-to-mysql

## Description

This repository has three scripts. wiktionary-downloader.sh is a bash script that downloads wiktionary entries from kaikki.org with wget. todb.py is a python script that parses the downloaded jsonl files and sends the information to a database. Finally, TDict.py is a TUI dictionary implementation of the database.

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
|-w [WORD], --word [WORD]|Search given word in dictionary|
|-p [part of speech], --pos [part of speech]|Specify a specific part of speech to search in|
|-e, --examples|Show examples|

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
