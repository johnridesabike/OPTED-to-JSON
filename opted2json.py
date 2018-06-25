#!/usr/bin/env python3
from html.parser import HTMLParser
import re
import json
import string
from os import path, listdir

OPTED_DIR = path.join('OPTED', 'v003')
OPTED_FILES = filter(lambda x: x.endswith('.html'), 
                    listdir(OPTED_DIR))
JSON_DIR = 'json'
trimdefs = re.compile('(^\) )|( \()')


class Opted2Json(HTMLParser):
    def __init__(self):
        ''' Dictionary object structured as:
        {"word": [ {"partOfSpeech": "noun", "text" : "definition one"},
                   {"partOfSpeech": "verb", "text" : "definition two"} ] 
        }
        '''
        self.dict = {}
        self.founddef = False
        self.foundword = False
        self.foundPOS = False
        self.currentword = ''
        self.currentdef = {}
        super().__init__()
        
    def handle_starttag(self, tag, attrs):
        if self.founddef:
            if tag == 'b':
                self.foundword = True
            if tag == 'i':
                self.foundPOS = True
        if tag == 'p':
            self.founddef = True
        
    def handle_endtag(self, tag):
        if self.foundword and tag == 'b':
            self.foundword = False
        if self.founddef and tag == 'p':
            self.founddef = False
        if self.foundPOS and tag == 'i':
            self.foundPOS = False
        
    def handle_data(self, data):
        if self.foundword:
            data = data.lower()
            self.currentword = data
            self.currentdef = {}
            if data not in self.dict:
                self.dict[data] = []
        if self.foundPOS:
            self.currentdef['partOfSpeech'] = data
        if self.founddef and not self.foundword and not self.foundPOS:
            data = trimdefs.sub('', data)
            if data:    
                if 'partOfSpeech' not in self.currentdef:
                    self.currentdef['partOfSpeech'] = ''
                self.currentdef['text'] = data
                self.dict[self.currentword].append(self.currentdef)

new = {}
for file in OPTED_FILES:
    letter = None
    letter_re = re.search('_(\w)\.', file)
    if letter_re:
        letter = letter_re.group(1)
    with open(path.join(OPTED_DIR, file), 'r', encoding='mac_roman') as f:
        parser = Opted2Json()
        parser.feed(f.read())
        if file == 'wb1913_new.html':
            # wb1913_new.html contains new words that need to be added to their
            # appropriate letter files
            new = parser.dict
        else:
            with open(path.join(JSON_DIR, letter + '.json'), 'w') as j:
                json.dump(parser.dict, j, indent=0)
            print("Converted", file, 'to', letter + '.json')
# sort the new words into their letters
letters = {k: {} for k in string.ascii_lowercase}
for word in new:
    alpha = re.sub('[^a-zA-Z]', '', word)[:1].lower()
    letters[alpha][word] = new[word]
# open the JSON files and update them with new words
for l in letters:
    with open(path.join(JSON_DIR, l + '.json'), 'r') as f:
        data = json.load(f)
    for word in letters[l]:
        # we can't just update() the dictionary because that would override
        # words that already have definitions. We want to add additional
        # definitions.
        if word in data:
            data[word] += letters[l][word]
        else:
            data[word] = letters[l][word]
    with open(path.join(JSON_DIR, l + '.json'), 'w') as f:
        json.dump(data, f, indent=0)
    print('Updated', l + '.json', 'with', len(letters[l]), 'new words')