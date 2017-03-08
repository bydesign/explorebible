import json, re, urllib, spacy
from firebase import Firebase
from slugify import slugify
import os.path

nlp = spacy.load('en')

### SETTINGS ###
PRINT_TREE = False
PRINT_JSON = True
PRINT_TRIPLES = False

# class to store and manipulate triple data
# generally this includes subject, verb, object triples
class Triple():
    def __init__(self, subj=None, verb=None, obj=None):
        self.subj = subj
        self.verb = verb
        self.obj = obj

    def __unicode__(self):
        if self.is_populated():
            subj = ''
            if self.subj:
                subj = self.subj.lemma_
            verb = ''
            if self.verb:
                verb = self.verb.lemma_
            obj = ''
            if self.obj:
                obj = self.obj.lemma_
            return '%s %s %s' % (subj, verb, obj)
        else:
            return ''

    def is_populated(self):
        count = 0
        if self.subj:
            count = count + 1
        if self.subj:
            count = count + 1
        if self.subj:
            count = count + 1

        print count
        return count >= 2
        #return bool(self.subj and self.verb and self.obj)

    def __str__(self):
        return self.__unicode__()

    def printobj(self):
        str = self.__unicode__()
        if str:
            print str

    def add_to_dict(self, json_dict):
        if self.is_populated():
            json_dict.add_triple(self)

class JsonPrinter():
    def __init__(self):
        self.obj = []
        self.triples = []

    def add_sentence(self):
        self.obj.append({
            'words': [],
            'root': None
        })

    def add_word(self, token):
        self.obj[-1]['words'].append({
            'word': unicode(token),
            'pos': token.pos_,
            'lemma': token.lemma_,
            'dep': token.dep_,
            'tag': token.tag_,
            'whitespace': token.whitespace_,
            'isPunct': token.is_punct
        })

    def add_triple(self, triple):
        self.triples.append({
            'subj': unicode(triple.subj),
            'verb': unicode(triple.verb),
            'obj': unicode(triple.obj)
        });

    def toJson(self):
        return json.dumps(self.obj, indent=4)

    def toFile(self):
        jsonfile = open('firebase/public/data/verse_data.json', 'w')
        jsonfile.write(self.toJson())
        jsonfile.close()

        jsonfile = open('firebase/public/data/triple_data.json', 'w')
        jsonfile.write(json.dumps(self.triples, indent=4))
        jsonfile.close()

    def __unicode__(self):
        return self.toJson()

    def __str__(self):
        return self.toJson()


verbs = ['root', 'ccomp', 'relcl']
subjects = ['nsubj']
objects = ['acomp','dobj']

def make_triples(token, parent_triple=None, level=0, conj_type=None, json_printer=None):
    triple = Triple()
    triples = [triple]

    if token.dep_.lower() in verbs:
        triple.verb = token

    for child in token.children:
        if child.dep_ in subjects:
            triple.subj = child
        elif child.dep_ in objects:
            triple.obj = child

        if child.dep_ == 'conj':
            # handle multiple subjects
            if token.dep_ in subjects or conj_type in subjects:
                trip = Triple(subj=child, verb=parent_triple.verb, obj=parent_triple.obj)
                if PRINT_TRIPLES: trip.printobj()
                trip.add_to_dict(json_printer)

            # handle multiple objects
            elif token.dep_ in objects or conj_type in objects:
                trip = Triple(subj=parent_triple.subj, verb=parent_triple.verb, obj=child)
                if PRINT_TRIPLES: trip.printobj()
                trip.add_to_dict(json_printer)

    if triple:
        if PRINT_TRIPLES: triple.printobj()
        triple.add_to_dict(json_printer)

    for child in token.children:
        lev_str = ' - '
        for i in range(level):
            lev_str += ' - '
        if PRINT_TREE:
            print u'%s%s (%s : %s)' % (lev_str, unicode(child), child.dep_, child.pos_.lower())

        child_conj_type = None
        if child.dep_ == 'conj':
            child_conj_type = conj_type or token.dep_
            triple = parent_triple

        child_triples = make_triples(child, triple, level+1, child_conj_type, json_printer=json_printer)
        if child_triples:
            triples = child_triples + triples

    strs = []
    for triple in triples:
        print triple
        trip_str = unicode(triple)
        if trip_str:
            strs.append(trip_str)
    return strs

NOPOS = ['PRON', 'CONJ', 'PUNCT']
NODEP = ['prep', 'det', 'poss', 'mark', 'neg']

def parse_bible(filename):
    text = open(filename).read().decode('utf8')
    text = text.replace('\n', ' ')
    text = text.replace('  ', ' ')
    json_printer = JsonPrinter()
    phrases_dict = {}

    nlp = spacy.load('en')

    doc = nlp(text)

    phrases = []

    for sent in doc.sents:
        prev_prev_word = None
        prev_word = None

        for idx, word in enumerate(sent):
            if word.dep_ not in NODEP and word.pos_ not in NOPOS:
                phrases.append(unicode(word))

        json_printer.add_sentence()
        sent_phrases = make_triples(sent.root, json_printer=json_printer)
        print sent_phrases
        phrases = phrases + sent_phrases

    for phrase in phrases:
        try:
            obj = phrases_dict[phrase]
            obj.count = obj.count + 1
        except KeyError:
            phrases_dict[phrase] = {
                'str': phrase,
                'count': 1
            }

        print phrase

    #print phrases_dict

    #print phrases

#parse_bible('data/john-3-16.txt')

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

p = re.compile(r'<.*?>')
q = re.compile(r'([,.:])(?![\s])')
def fixtxt(data):
    data = data.replace('  ', ' ')
    data = p.sub('', data)
    #data = q.sub(r'\1 ', data)
    return data

SEARCH_DICT = {}
SEARCH_LIST = []
PHRASE_DICT = {}
PHRASE_LIST = []
def add_phrase(phrase, verse):
    vobj = {
        'id': verse['name'],
        #'text': verse['span'].text,
        'name': verse['name']
    }
    if phrase not in PHRASE_DICT:
        obj = {
            'text': phrase,
            'count': 1,
            'verses': [vobj]
        }
        PHRASE_DICT[phrase] = obj
        PHRASE_LIST.append(obj)

        sobj = {
            'text': phrase,
            'count': 1
        }
        SEARCH_DICT[phrase] = sobj
        SEARCH_LIST.append(sobj)

    else:
        obj = PHRASE_DICT[phrase]
        obj['count'] += 1
        obj['verses'].append(vobj)
        SEARCH_DICT[phrase]['count'] += 1

def save_file(path, content):
    jsonfile = open(path, 'w')
    jsonfile.write(content)
    jsonfile.close()
    print 'saved file '+path

def get_chapter(bookname, chapter):
    filename = '%s %d' % (bookname, chapter)
    print filename
    path = 'firebase/public/data/net/'+ filename +'.json'
    response = open(path).read()
    print 'found file '+path

    return json.loads(response)

def save_list(l, url, path):
    print 'saving %d phrases ...' % len(l)
    f = Firebase(url)
    f.delete()
    phrasedict = {}
    printphrases = []
    for i, s in enumerate(l):
        key = slugify(s['text'])
        if key:
            phrasedict[key] = s
            f.push(s)
            printphrases.append(key)
        if i % 20 == 0:
            print ', '.join(printphrases)
            printphrases = []
    save_file(path, json.dumps(phrasedict))
    print 'Saved %d phrases ...' % len(l)


def download_book(bookname, chapter_count, start_chapter=1):
    book_json = []

    # load book chapters
    for ch in range(chapter_count):
        chnum = ch + start_chapter
        book_json = get_chapter(bookname, chnum)
        book_parts = []
        for verse in book_json:
            book_parts.append(verse['text'])

        bookstr = ' '.join(book_parts)

        bookstr = fixtxt(bookstr)
        doc = nlp(bookstr)

        words = []
        for sent in doc.sents:
            prev_prev_word = None
            prev_word = None

            for word in sent:
                words.append(unicode(word))
                #print word

        verse_positions = []
        token_first = 0
        token_last = 0
        tokens = []
        for verse in book_json:
            token_first = len(tokens)
            token = ''
            for char in fixtxt(verse['text']):
                if char.isalnum():
                    token += char
                else:
                    if token:
                        tokens.append(token)
                    token = ''
                    if not char.isspace():
                        tokens.append(char)

            token_last = len(tokens)
            verse_id = 'en/net/%s/%s/%s' % (slugify(verse['bookname']), verse['chapter'], verse['verse'])
            verse_name = '%s %s:%s' % (verse['bookname'], verse['chapter'], verse['verse'])
            span = doc[token_first : token_last]
            verse_positions.append({
                'id': verse_id,
                'span': span,
                'name': verse_name,
                'num': verse['verse'],
                'pretitle': verse['title']
            })

        chapdict = {
            'name': '%s %s' % (bookname, chnum),
            'verses': []
        }
        for v in verse_positions:
            vdict = {
                'n': v['num'],
                't': []
            }
            chapdict['verses'].append(vdict)
            tokens = vdict['t']
            for word in v['span']:
                token = {
                    't': unicode(word)   # word text
                }
                if word.is_punct:
                    token['p'] = word.is_punct # is punctuation

                if not word.is_punct:
                    if unicode(word) != word.lemma_:
                        token['l'] = word.lemma_        # lemma root word
                    if word.is_title:
                        token['h'] = word.is_title # is title / heading
                    token['s'] = word.pos          # part of speech
                    #token['d'] = word.dep_          # dep
                    #token['g'] = word.tag_,         # tag
                    #token['tw'] = word.text_with_ws,    # text with whitespace

                if word.whitespace_ == ' ':
                    token['w'] = word.whitespace_   # whitespace

                tokens.append(token)

                if word.dep_ not in NODEP and word.pos_ not in NOPOS:
                    add_phrase(word.lemma_, v)

            #vdict['length'] = len(tokens)

        chapid = 'en/net/%s/%s' % (slugify(bookname), chnum)
        f = Firebase('https://project-6084703088352496772.firebaseio.com/' + chapid)
        f.put(chapdict)
        path = 'firebase/public/data/net_parsed/%s-%d.json' % (slugify(bookname), chnum)
        save_file(path, json.dumps(chapdict, separators=(',', ':')))
        print 'Saving %s ...' % chapid

    searchdict = {}
    for s in SEARCH_LIST:
        key = slugify(s['text'])
        if key:
            searchdict[key] = s

    #save_file('firebase/public/data/search/search_terms.json', json.dumps(searchdict))
    #print 'Saving %d search terms ...' % len(SEARCH_LIST)
    #f = Firebase('https://project-6084703088352496772.firebaseio.com/search/')
    #f.put(searchdict)

    #url = 'https://project-6084703088352496772.firebaseio.com/phrases/'
    #path = 'firebase/public/data/search/search_phrases.json'
    #save_list(PHRASE_LIST, url, path)


download_book('Matthew', 28, 1)



def upload_divisions():
    books_file = open('firebase/public/data/books.json')
    divs = json.load(books_file)
    f = Firebase('https://project-6084703088352496772.firebaseio.com/books/en/')
    f.put(divs)

#upload_divisions()
