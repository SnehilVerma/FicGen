import requests
from bs4 import BeautifulSoup
import json

""" URL = "http://downloads.cs.stanford.edu/nlp/data/coqa/coqa-train-v1.0.json"
r = requests.get(URL)
  
soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
#print(soup.prettify())

with open("Coqa.json", "w") as file:
    file.write(str(soup)) """

f = open("Coqa.json","r+", encoding="utf-8")
data = json.load(f)["data"]

story = {}
for i in range(len(data)):
    story[i] = "<|BOS|>" + data[i]["story"] + "<|EOS|>"

with open("coqa_story.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(story))
