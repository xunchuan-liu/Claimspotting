import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion") #Testing splitting of words


for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

doc = nlp("Autonomous cars shift insurance liability toward manufacturers") #Testing noun chunks
for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_,
            chunk.root.head.text)

doc = nlp("Apple is looking at buying U.K. startup for $1 billion") #Testing named entity recognition, recognizes what kind of word each is IMPORTANT
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)