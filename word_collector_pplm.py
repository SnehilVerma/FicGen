import json
import pprint as pp


f = open('book_backtranslate.json','r')
data = json.load(f)

sci_fi_set = set()
for k,v in data.items():
    for word in v["keywords"]:
        sci_fi_set.add(word)


pp.pprint(sci_fi_set)
f.close()
f = open('pplm_wordset.txt','r+')
json.dump(list(sci_fi_set),f)


