import spacy
nlp = spacy.load('en')

class Triple():
    def __init__(self, subj=None, verb=None, obj=None):
        self.subj = subj
        self.verb = verb
        self.obj = obj

    def __unicode__(self):
        return '------------------\n%s -> %s -> %s\n------------------' % (self.subj, self.verb, self.obj)

    def __str__(self):
        return self.__unicode__()

verbs = ['root', 'ccomp', 'relcl']
subjects = ['nsubj']
objects = ['acomp','dobj']
def make_triple(token, parent_triple=None, level=0, conj_type=None):
    triple = None
    #print token.dep_
    if token.dep_.lower() in verbs:
        triple = Triple(verb=token)
        triples = [triple]

    for child in token.children:
        if child.dep_ in subjects:
            triple.subj = child
        elif child.dep_ in objects:
            triple.obj = child

        if child.dep_ == 'conj':
            # handle multiple subjects
            if token.dep_ in subjects or conj_type in subjects:
                trip = Triple(subj=child, verb=parent_triple.verb, obj=parent_triple.obj)
                print trip

            # handle multiple objects
            elif token.dep_ in objects or conj_type in objects:
                trip = Triple(subj=parent_triple.subj, verb=parent_triple.verb, obj=child)
                print trip

    if triple: print triple

    for child in token.children:
        lev_str = ' - '
        for i in range(level):
            lev_str += ' - '
        print u'%s%s (%s : %s)' % (lev_str, unicode(child), child.dep_, child.pos_.lower())

        child_conj_type = None
        if child.dep_ == 'conj':
            child_conj_type = conj_type or token.dep_
            triple = parent_triple
        make_triple(child, triple, level+1, child_conj_type)

    #return triples

def parse_chapter(filename):
    text = open(filename).read().decode('utf8')
    text = text.replace('\n', '')
    doc = nlp(text)
    triples = []

    for sent in doc.sents:
        root = sent.root
        print u'\n\n------------------------\n%s (%s : %s)' % (unicode(root), root.dep_.lower(), root.pos_.lower())
        make_triple(sent.root)
        '''triple = Triple(verb=unicode(sent.root))
        for child in sent.root.children:
            if child.dep_ == 'nsubj':
                triple.subj = child
            elif child.dep_ == 'acomp' or child.dep_ == 'dobj':
                triple.obj = child

            elif child.dep_ == 'ccomp':
                trip = Triple(verb=child)

            print u' - %s (%s)' % (unicode(child), child.dep_)

            for ch in child.children:
                if child.dep_ == 'acomp' or child.dep_ == 'dobj':
                    if ch.dep_ == 'conj':
                        trip = Triple(subj=triple.subj, verb=triple.verb, obj=ch)
                        print trip
                        triples.append(trip)
                print u' - - %s (%s)' % (unicode(ch), ch.dep_)

                for i in ch.children:
                    print u' - - - %s (%s)' % (unicode(i), i.dep_)
            #print child.dep_

        print triple
        triples.append(triple)'''

#    for token in doc:
#        print token

#    for token in tokens:
#        print token

    return doc

## run
parse_chapter('bible-tests.txt')
