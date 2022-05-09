import json
from typing import final
from googletrans import Translator
from langcodes import Language




languages = [
    'en', # english
    'es', # spanish
    'it', # italian
    ]


SPECIAL_TOKENS  = { "bos_token": "<|BOS|>",
                    "eos_token": "<|EOS|>",
                    "unk_token": "<|UNK|>",                    
                    "pad_token": "<|PAD|>",
                    "sep_token": "<|SEP|>"}


try:
    f = open("book_backtranslate.json",'r+')
    data = json.load(f)

    translator = Translator()
    f2 = open('books_dataset_2.json','r+')
    json_set = json.load(f2)
    f2.close()

    f3 = open('global_vars.json','r+')
    json_vars = json.load(f3)

    for entry in data.keys():
        if json_vars['data']['books_processed'] >= 145 :
            break
        if entry in json_vars['data']['books_processed_list']:
            continue
        
        print(json_vars['data']['books_processed'])
        print(entry)
        
        t = translator.translate(data[entry]['plot'],src='en',dest=languages[0])    
        t2 = translator.translate(t.text,src=languages[0],dest=languages[1])
        t3 = translator.translate(t2.text,src=languages[1],dest=languages[2])
        pp = translator.translate(t3.text,src=languages[2],dest='en')
        
        keywords_new = []
        for word in data[entry]['keywords']:
            t = translator.translate(word,src='en',dest=languages[0])    
            t2 = translator.translate(t.text,src=languages[0],dest=languages[1])
            t3 = translator.translate(t2.text,src=languages[1],dest=languages[2])
            pp = translator.translate(t3.text,src=languages[2],dest='en')
            keywords_new.append(pp.text)

        key_entry = f'{entry}' + '_aug'
        json_set["books"].append({str(key_entry): str(SPECIAL_TOKENS["bos_token"] + entry + SPECIAL_TOKENS["sep_token"] + " ".join(keywords_new) + SPECIAL_TOKENS["sep_token"] + data[entry]['plot'] + SPECIAL_TOKENS["eos_token"])})
        # print(len(json_set))
        json_vars['data']['books_processed_list'].append(entry)
        json_vars['data']['books_processed'] += 1
    
    f3.close()
    f3 = open('global_vars.json','w+')
    json.dump(json_vars,f3)
    f3.close()
    # print(json_set)
    f2 = open('books_dataset_2.json','w+') 
    json.dump(json_set,f2)
except Exception as e:
    print('here')
    print(e)
    f3.close()
    f3 = open('global_vars.json','w+')
    json.dump(json_vars,f3)
    # print(json_set)
    f2 = open('books_dataset_2.json','w+') 
    json.dump(json_set,f2)
finally:
    f3.close()
    f2.close()
    f.close()



f = open('books_dataset.json','r+')
f2 = open('books_dataset_2.json','r')
aug_list = json.load(f2)["books"]
og_dict = json.load(f)
for aug_book in aug_list:
    for k,v in aug_book.items():
        og_dict[k] = v


json.dump(og_dict,f)
f.close()
f2.close()
