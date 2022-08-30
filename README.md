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

## How to fetch underlying JSON objects:
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
