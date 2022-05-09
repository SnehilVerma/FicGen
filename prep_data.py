import json
import pprint as pp
import pytextrank
import spacy
from textblob import TextBlob
# from bs4 import BeautifulSoup
import requests
import wikipedia
import re


not_found = 0
'''
Links:
1) https://aneesha.medium.com/beyond-bag-of-words-using-pytextrank-to-find-phrases-and-summarize-text-f736fa3773c5
2) https://towardsdatascience.com/textrank-for-keyword-extraction-by-python-c0bae21bcec0
'''
'''
def get_summary():
    page = requests.get("https://en.wikipedia.org/wiki/The_Island_of_Doctor_Moreau#Plot")
    soup = BeautifulSoup(page.content, 'html.parser')
    

    print(soup.prettify())
    # heading = soup.find(id='Plot')
    # print(heading)

    # teams = heading.find_next('p')
    # for team in teams:
    #     print(team.string)
'''

def get_summary_wikipedia(title):
    try:
        wiki = wikipedia.page(title)
    except:

        return None
    # wiki = wikipedia.page('The Time Machine')
    # Extract the plain text content of the page
    text = wiki.content
    # very important to understand this regex.
    # explain the regex.
    

    plot_keywords = ['Plot','Plot summary','Plot synopsis','Main story','Story','Plot overview','Synopsis','Plot introduction']
    result = None
    for kw in plot_keywords:
        if result is None:
            result = re.search(f'=+ {kw} =+\n+((.|\n)*?)=+',text)
        else:
            break

        
    # result = re.search(f'== {plot_keywords[0]} ==\n+((.|\n)*?)==',text)
    
    if result is None:
        print(title)
        return result
    # print(result.group(1))
    return result.group(1)


def get_rank(plot):
    nlp = spacy.load("en_core_web_sm")

    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank")
    # nlp.add_pipe("positionrank")
    doc = nlp(plot)

    mid_doc = []

    exclusion_list = []
    for token in doc:
        if token.pos_ == 'PROPN':
            exclusion_list.append(token.text)

    # print(exclusion_list)

    # for noun in doc.noun_chunks:
    #     if noun.root.pos_ != "PROPN":
    #         mid_doc.append(noun.root.text)
    
    # top ranked phrases
    for phrase in doc._.phrases:
        pwords = phrase.text.split(' ')
        for w in pwords:
            if w in exclusion_list:
                continue
            if w not in mid_doc:
                mid_doc.append(w)
        # mid_doc.append(phrase.text)

    
    # print(mid_doc)
    return mid_doc[:20]



def read_sf_gram():
    f = open("SFGram-dataset/books.json","r+")
    sf_dict = json.load(f)["books"]

    print(len(sf_dict))

    # res = get_summary_wikipedia('Triplanetary (novel)')
    # res = get_summary_wikipedia("Starman's Quest")
    # exit()
    
    t_count = 0
    wiki_count = 0
    for book in sf_dict:
        if 'wikipedia' in book.keys():
            wiki_count += 1
            if 'found' in book["wikipedia"].keys():
                if book["wikipedia"]["found"] is True:
                    t_count += 1
                    if 'original_title' in book.keys():
                        title = book['original_title']
                    else:
                        title = book["title"]

                    if 'plot' in book.keys():
                        keywords = get_rank(book['plot'])
                        book["keywords"] = keywords
                    else:
                        plot = get_summary_wikipedia(title)
                        if plot is None:
                            # if unable to crawl for this book's plot, skip.
                            continue
                        book["plot"] = plot
                        keywords = get_rank(plot)
                        book["keywords"] = keywords

    SPECIAL_TOKENS  = { "bos_token": "<|BOS|>",
                    "eos_token": "<|EOS|>",
                    "unk_token": "<|UNK|>",                    
                    "pad_token": "<|PAD|>",
                    "sep_token": "<|SEP|>"}
    print('tcount',t_count)
    print('wikicount',wiki_count)
    count = 0
    json_output = {}
    json_dumput = {}
    for book in sf_dict:
        if 'keywords' in book.keys():
            count = count + 1
            json_output[book["title"]] = SPECIAL_TOKENS["bos_token"] + book["title"] + SPECIAL_TOKENS["sep_token"] + " ".join(book["keywords"]) + SPECIAL_TOKENS["sep_token"] + book["plot"] + SPECIAL_TOKENS["eos_token"]
            json_dumput[book["title"]] = {"plot":book["plot"],"keywords":book["keywords"]}
        

    
    f = open("books_dataset.json","w+")
    json.dump(json_output,f)
    f.close()

    f = open("book_backtranslate.json","w+")
    json.dump(json_dumput,f)

    print(count)

if __name__ == '__main__':
    read_sf_gram()