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
    doc = nlp(plot)

    mid_doc = []
    for noun in doc.noun_chunks:
        mid_doc.append(noun.text)
    
    x = ' '.join(mid_doc)
    doc = nlp(x)
    
    # examine the top-ranked phrases in the document
    phrase_ranks = []
    for phrase in doc._.phrases:
        phrase_ranks.append((phrase.rank,phrase.text))
    
    return phrase_ranks[:10]



def read_sf_gram():
    f = open("SFGram-dataset/books.json","r+")
    sf_dict = json.load(f)["books"]

    print(len(sf_dict))

    # res = get_summary_wikipedia('Triplanetary (novel)')
    # res = get_summary_wikipedia("Starman's Quest")
    # exit()
    
    t_count = 0
    for book in sf_dict:
        if 'original_title' not in book.keys():
            continue
        title = book['title']
        # if title is not None:
        #     t_count = t_count + 1

        if 'plot' in book.keys():
            get_rank(book['plot'])
            keywords = get_rank(book['plot'])
            book["keywords"] = keywords
        else:
            plot = get_summary_wikipedia(title)
            if plot is None:
                # if unable to crawl for this book's plot, skip.
                continue
            keywords = get_rank(plot)
            book["keywords"] = keywords
    
    # print('tcount',t_count)
    count = 0
    for book in sf_dict:
        if 'keywords' in book.keys():
            count = count + 1
            # print(book["keywords"])
    
    print(count)

if __name__ == '__main__':
    read_sf_gram()