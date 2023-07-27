# via json api ("q" instead of "query")
import os, sys, requests
import json

def normalize(v):
    return list(map(lambda x: float("%.4f" % x), v))

from sentence_transformers import SentenceTransformer

def do_search(debug=False):
    model = SentenceTransformer('all-mpnet-base-v2')
    sentence = input("Input ? ")
    embeddings = model.encode([sentence])
    v = normalize(embeddings.tolist()[0])

    # json query api should use "query" but "q"?
    params = {
    "q": "{!knn f=vector topK=3}" + repr(v)
    }
    r = requests.post('http://localhost:8983/solr/vector_test/query?fl=id,text', data=params)
    if debug:
        # print as is
        print(json.dumps(r.json(), indent = 2))
        pass
    else:
        docs = r.json().get('response', {}).get('docs', [])
        if len(docs) == 0:
            print("No document is returned")
        else:
            print(json.dumps(docs, indent = 2))
            pass
        pass
    pass

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    debug = False
    if args.debug:
        debug = True
        pass
    do_search(debug)
    pass

if __name__ == "__main__":

    main()
    pass
