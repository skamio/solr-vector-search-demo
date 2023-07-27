# Reference https://www.pinecone.io/learn/series/nlp/dense-vector-embeddings-nlp/
import sys
import json

def makedoc(i, sentence):
    embeddings = model.encode([sentence])
    v = embeddings.tolist()[0]
    d = {
        "id": i,
        "text": sentence,
        "vector": v
        }
    return d

    
sentences = [
    "canberra is the capital city of australia",
    "what is the capital city of australia?",
    "the capital city of france is paris",
    "the capital city of japan is tokyo",
    "the capital city of U.K. is london",
    "the capital city of Foo is Bar",
    "the population of paris is 2 million",
    "the population of london is 9.5 million",
    "the population of N.Y. is 8.1 million",
    "the population of Bar is 100",
    "the summer is hot",
    "winter jacket is for winter",
    "short pants are for summer",
]

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')
embeddings = model.encode(sentences)

docs = []
for i in range(len(sentences)):
    d = makedoc(i, sentences[i])
    docs.append(d)
    pass

json.dump(docs, sys.stdout)
