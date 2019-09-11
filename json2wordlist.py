import json
import string
from os import path

JSON_DIR = 'json'
TXT_DIR = 'txt'

for l in string.ascii_lowercase:
  with open(path.join(JSON_DIR, l + '.json'), 'r') as f:
    words = "\n".join(json.load(f).keys())
  with open(path.join(TXT_DIR, 'words.txt'), 'a') as f:
    f.writelines(words)