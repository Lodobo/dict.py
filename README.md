# wiktionary-to-mysql

## Description

This repository has two scripts. First, a bash script that downloads wiktionary entries from kaikki.org with wget to a .jsonl file. Second, a python script that parses the jsonl files and sends the information to a database.

Each jsonl file corresponds to a part of speech (e.g. nouns). The script will create a table for each part of speech.

I recommend running the following mysql code to each table to delete words that are too long:

```sql
DELETE FROM db.tble WHERE LENGTH(word) > 30;
```

And the following to change the type of the column:

```sql
ALTER TABLE db.tble MODIFY word char(30);
```

Warning: the jsonl files will consume a bit over 1gb of storage.

## Dependencies:

- wget
- pandas
- cryptography
- sqlalchemy
- alive_progress
- pymysql
- mysql
