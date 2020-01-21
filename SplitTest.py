import spacy
from pysbd.utils import PySBDFactory

nlp = spacy.blank('en')

# explicitly adding component to pipeline
# (recommended - makes it more readable to tell what's going on)
nlp.add_pipe(PySBDFactory(nlp))

# or you can use it implicitly with keyword
# pysbd = nlp.create_pipe('pysbd')
# nlp.add_pipe(pysbd)

doc = nlp('My name is Jonas E. Smith. Please turn to p. 55.')
print(list(doc.sents))
# [My name is Jonas E. Smith., Please turn to p. 55.]
