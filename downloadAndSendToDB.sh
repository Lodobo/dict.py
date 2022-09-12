#!/usr/bin/env bash


# English (en)
# French (fr)
# Swedish (sv)
# Latin (la)
# Spanish (es)
# German (de)
# Italian (it)
# Russian (ru)
# Finnish (fi)
# Arabic (ar)
# Dutch (nl)
# Norwegian (no)
# Danish (da)
# Northern sami (se)

en_abbrev="https://kaikki.org/dictionary/English/by-pos/abbrev/kaikki.org-dictionary-English-by-pos-abbrev.js--ZhTPI"
en_article="https://kaikki.org/dictionary/English/by-pos/article/kaikki.org-dictionary-English-by-pos-article.-D2bSFf"
en_conj="https://kaikki.org/dictionary/English/by-pos/conj/kaikki.org-dictionary-English-by-pos-conj.json"
en_det="https://kaikki.org/dictionary/English/by-pos/det/kaikki.org-dictionary-English-by-pos-det.json"
en_particle="https://kaikki.org/dictionary/English/by-pos/particle/kaikki.org-dictionary-English-by-pos-particl-akjezE"
en_prep="https://kaikki.org/dictionary/English/by-pos/prep/kaikki.org-dictionary-English-by-pos-prep.json"
en_pron="https://kaikki.org/dictionary/English/by-pos/pron/kaikki.org-dictionary-English-by-pos-pron.json"
en_adv="https://kaikki.org/dictionary/English/by-pos/adv/kaikki.org-dictionary-English-by-pos-adv.json "
en_adj="ttps://kaikki.org/dictionary/English/by-pos/adj/kaikki.org-dictionary-English-by-pos-adj.json"
en_verb="https://kaikki.org/dictionary/English/by-pos/verb/kaikki.org-dictionary-English-by-pos-verb.json"
en_noun="https://kaikki.org/dictionary/English/by-pos/noun/kaikki.org-dictionary-English-by-pos-noun.json"
en_all="https://kaikki.org/dictionary/English/kaikki.org-dictionary-English.json"

fr="https://kaikki.org/dictionary/French/kaikki.org-dictionary-French.json"
sv="https://kaikki.org/dictionary/Swedish/kaikki.org-dictionary-Swedish.json"
la="https://kaikki.org/dictionary/Latin/kaikki.org-dictionary-Latin.json"
es="https://kaikki.org/dictionary/Spanish/kaikki.org-dictionary-Spanish.json"
de="https://kaikki.org/dictionary/German/kaikki.org-dictionary-German.json"
it="https://kaikki.org/dictionary/Italian/kaikki.org-dictionary-Italian.json"
ru="https://kaikki.org/dictionary/Russian/kaikki.org-dictionary-Russian.json"
fi="https://kaikki.org/dictionary/Finnish/kaikki.org-dictionary-Finnish.json"
ar="https://kaikki.org/dictionary/Arabic/kaikki.org-dictionary-Arabic.json"
nl="https://kaikki.org/dictionary/Dutch/kaikki.org-dictionary-Dutch.json"
no="https://kaikki.org/dictionary/Norwegian/kaikki.org-dictionary-Norwegian.json"
da="https://kaikki.org/dictionary/Danish/kaikki.org-dictionary-Danish.json"
se="https://kaikki.org/dictionary/Northern%20Sami/kaikki.org-dictionary-NorthernSami.json"


# solution : for item in array if statement.

dir="$(pwd)"

# Create directory if it doesn't exist
[ ! -d jsonfiles ] && mkdir jsonfiles

cd jsonfiles

for i in $@
do
	if  [ $i == "en" ]
	then
		wget --output-document="en_abbreviations.jsonl" ${en_abbrev}
		wget --output-document="en_articles.jsonl" ${en_article}
		wget --output-document="en_conjunctions.jsonl" ${en_conj}
		wget --output-document="en_determiners.jsonl" ${en_det}
		wget --output-document="en_particles.jsonl" ${en_particle}
		wget --output-document="en_prepositions.jsonl" ${en_prep}
		wget --output-document="en_pronouns.jsonl" ${en_pron}
		wget --output-document="en_adverbs.jsonl" ${en_adv}
		wget --output-document="en_adjectives.jsonl" ${en_adj}
		wget --output-document="en_verbs.jsonl" ${en_verb}
		wget --output-document="en_nouns.jsonl" ${en_noun}
		wget --output-document="en_all.jsonl" ${en_all}	
		python3 $dir/todb.py -l en
	elif [ $i == "fr" ]
	then
		wget --output-document="fr.jsonl" ${fr}
		python3 $dir/todb.py -l fr
	elif [ $i == "sv" ]
	then
		wget --output-document="sv.jsonl" ${sv}
		python3 $dir/todb.py -l sv
	elif [ $i == "la" ]
	then
		wget --output-document="la.jsonl" ${la}
		python3 $dir/todb.py -l la
	elif [ $i == "es" ]
	then
		wget --output-document="es.jsonl" ${es}
		python3 $dir/todb.py -l es
	elif [ $i == "it" ]
	then
		wget --output-document="it.jsonl" ${it}
		python3 $dir/todb.py -l it
	elif [ $i == "de" ]
	then
		wget --output-document="de.jsonl" ${de}
		python3 $dir/todb.py -l de
	elif [ $i == "ru" ]
	then
		wget --output-document="ru.jsonl" ${ru}
		python3 $dir/todb.py -l ru
	elif [ $i == "fi" ]
	then
		wget --output-document="fi.jsonl" ${fi}
		python3 $dir/todb.py -l fi
	elif [ $i == "ar" ]
	then
		wget --output-document="ar.jsonl" ${ar}
		python3 $dir/todb.py -l ar
	elif [ $i == "nl" ]
	then
		wget --output-document="nl.jsonl" ${nl}
		python3 $dir/todb.py -l nl
	elif [ $i == "no" ]
	then
		wget --output-document="no.jsonl" ${no}
		python3 $dir/todb.py -l no
	elif [ $i == "da" ]
	then
		wget --output-document="da.jsonl" ${da}
		python3 $dir/todb.py -l da
	elif [ $i == "se" ]
	then
		wget --output-document="se.jsonl" ${se}
		python3 $dir/todb.py -l se
	else
		echo "expected at least one argument"
		echo "Usage : [script.sh en fr sv]"
	fi
done


