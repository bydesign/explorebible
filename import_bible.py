import json, re, urllib, spacy
from firebase import Firebase
from slugify import slugify
import os.path

def save_file(path, content):
    jsonfile = open(path, 'w')
    jsonfile.write(content)
    jsonfile.close()
    print 'saved file '+path

def download_chapter(bookname, chapter):
    filename = '%s %d' % (bookname, chapter)
    print filename
    path = 'firebase/public/data/net/'+ filename +'.json'
    response = ''
    print path
    if os.path.isfile(path):
        response = open(path).read()
        print 'found file '+path

    else:
        url = 'http://labs.bible.org/api/?passage='+ filename +'&type=json'
        response = urllib.urlopen(url).read()
        save_file(path, response)

    return json.loads(response)

def run():
    filename = 'firebase/public/data/books.json'
    biblefile = open(filename).read()
    bible = json.loads(biblefile)
    for div in bible:
        for book in div['books']:
            bookname = book['name']
            chapters = []
            
            for chap in range(book['ct']):
                chnum = chap + 1
                name = '%s %d' % (bookname, chnum)
                print 'Getting ' + name
                chapdata = download_chapter(bookname, chnum)
                versecount = len(chapdata)

                chapters.append({
                    'num': chnum,
                    'ct': versecount
                })

            book['chs'] = chapters
            del book['chapters']

    save_file(filename, json.dumps(bible, indent=4))

    f = Firebase('https://project-6084703088352496772.firebaseio.com/books/en/')
    f.delete()
    f.put(bible)

    print 'saved updated verse counts'
run()
