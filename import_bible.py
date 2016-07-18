import json, re, urllib, spacy
from firebase import Firebase
from slugify import slugify
import os.path
import time, random

def save_file(path, content):
    jsonfile = open(path, 'w')
    jsonfile.write(content)
    jsonfile.close()
    print 'saved file '+path

def download_chapter(bookname, chapter):
    filename = '%s %d' % (bookname, chapter)
    path = 'firebase/public/data/net/'+ filename +'.json'
    response = ''
    if os.path.isfile(path):
        response = open(path).read()
        print 'found file '+path

    else:
        url = 'http://labs.bible.org/api/?passage='+ filename +'&type=json'
        print url
        response = urllib.urlopen(url).read()
        save_file(path, response)

        time.sleep(random.randint(0,2))

    return json.loads(response)

def upload_chapters():
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
                print '--------------\nGetting ' + name
                chapdata = download_chapter(bookname, chnum)
                #versecount = len(chapdata)
                wordcounts = []
                for v in chapdata:
                    if 'title' in v:
                        wordcounts.append(v['title'])
                    wordcount = len(v['text'].split(' '))
                    wordcounts.append(wordcount)

                print wordcounts
                chapters.append({
                    'num': chnum,
                    'ct': wordcounts
                })

            book['chs'] = chapters

            if 'chapters' in book:
                del book['chapters']

    save_file(filename, json.dumps(bible, indent=4))

    f = Firebase('https://project-6084703088352496772.firebaseio.com/chapters/en/net/')
    f.delete()
    f.put(bible)

    print 'saved updated verse counts'

def upload_books():
    filename = 'firebase/public/data/bible.json'
    biblefile = open(filename).read()
    bible = json.loads(biblefile)
    f = Firebase('https://project-6084703088352496772.firebaseio.com/books/en/')
    f.delete()
    f.put(bible)
    print 'saved books'

upload_chapters()
upload_books()
