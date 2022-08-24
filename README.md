# wiktionary-to-mysql

## Description

This repository has two scripts. First, a bash script that downloads wiktionary entries from kaikki.org with wget to a .jsonl file. Second, a python script that parses the jsonl files and sends the information to a database.

Each jsonl file corresponds to a part of speech (e.g. nouns). The script will create a table for each part of speech.

Each jsonl line has the following general structure:

```
{"pos": "",
"head_templates": [],
"forms": [],
"etymology_text": "",
"etymology_templates": [],
"sounds": [],
"word": "",
"lang": "",
"lang_code": "",
"senses": [],
"wikipedia": []}
```

The mysql database will create tables with  the following structure:

| Field               | Type   |
| ------------------- | ------ |
| index               | bigint |
| pos                 | text   |
| head_templates      | json   |
| etymology_text      | text   |
| etymology_templates | json   |
| sounds              | json   |
| forms               | json   |
| word                | text   |
| lang                | text   |
| land_code           | text   |
| senses              | json   |
| wikipedia           | json   |


The python script works but still needs some changes. Ideally the 'word' column should be the primary key and no duplicate entries should exist. I recommend running the following mysql code to each table to delete words that are too long:

```sql
DELETE FROM db.tble WHERE LENGTH(word) > 30;
```

And the following to change the type of the column:

```sql
ALTER TABLE db.tble MODIFY word char(30);
```

Warning: the jsonl files will consume a bit over 1gb of storage. Some of the longer jsonl files, such as the noun and verb files, take very long to parse : possibly over an hour.

## Dependencies:

- -wget
- jsonlines
- pandas
- cryptography
- sqlalchemy
- tqdm
- pymysql
- mysql
