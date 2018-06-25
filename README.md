# OPTED to JSON Converter

The [Online Plain Text English Dictionary (OPTED)](http://www.mso.anu.edu.au/~ralph/OPTED/index.html) is a public domain dictionary based on [Project Gutenberg's digitization of the 1913 Webster Unabridged Dictionary](https://www.gutenberg.org/ebooks/29765).

This is a Python script that converts the OPTED from HTML to JSON. The code can probably be modified to convert the OPTED to other formats as well.

Outputted files are written to the `/json/` directory. They're separated into a file for each letter. The structure of the JSON data is an object with the words as names and the values are arrays of definitions. Each definition is an object with the part of speech and definition text. See this example:

```
{"word": [ {"partOfSpeech": "noun", "text" : "definition one"},
            {"partOfSpeech": "verb", "text" : "definition two"} ] 
}
```

There are several other scripts out there that convert the Webster Unabridged Dictionary to different formats. I wasn't satisfied with any of the ones I found, so I wrote my own.

Depending on your needs, the [GNU Collaborative International Dictionary of English (GCIDE)](http://gcide.gnu.org.ua) may be more useful, since it's much more complete. It's licensed under the GPL, so it does come with conditions for its use. The text of the OPTED is public domain.

The Python code portion of this repository is MIT licensed.