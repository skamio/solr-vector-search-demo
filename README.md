# solr-vector-search-demo

## Motivation

I compiled scripts to create a vector search with Apache Solr because I couldn't find end-to-end demo of Solr vector search.
It is also to learn vector search feature myself.

## Overview

Following scripts set up Solr with vector search schema.
Hugging Face sentence transformer is used to generate vectors.

## Environment

I tested these scripts on M1 Macbook.
Used software versions are followings:
- Apache Solr 9.2.1
- python 3.11.4
- Conda 4.10.1

I don't explain much of Solr basics here.
You can refer to [Apache Solr tutorial](https://solr.apache.org/guide/solr/latest/getting-started/solr-tutorial.html) if you need introduction.

## Steps

###
1. Prepare env

```shell
conda create -n sentence-transformers
pip install sentence-transformers
```

2. Make docs

In order to use vector search, each document has to be represented with vectors.
You can find the specification in solr doc.
https://solr.apache.org/guide/solr/latest/query-guide/dense-vector-search.html

I referenced the following site how to create vectors by using sentence transformers.
https://www.pinecone.io/learn/series/nlp/dense-vector-embeddings-nlp/
I used sentence transformer model `all-mpnet-base-v2` in the script.

Script 'make_docs.py' generates Solr documents which has `id`, `text` and `vector` fields.
The `vector` field contains vector representation of the `text`.

```shell
python3 make_docs.py > docs.json
```

3. Setup solr

Download apache solr: https://solr.apache.org/downloads.html 
Please refer to the detail in [the tutorial](https://solr.apache.org/guide/solr/latest/getting-started/solr-tutorial.html) or [official documentation](https://solr.apache.org/guide/solr/latest/index.html).

If you start locally in Unix or Mac, you can run as:
`bin/solr start -c`

You need to create a new collection in Solr which store search index.

```shell
sh ./create-collection.sh
```

But this collection only has default fields.
I need to add a vector field.
The following script adds a vector field definition.

```shell
sh ./update-schema.sh
```

Solr vector search feature is called "dense vector search".
You can find the reference in https://solr.apache.org/guide/solr/latest/query-guide/dense-vector-search.html

Vector field definition in this schema is as follows:
```json
  "add-field-type": {
    "name": "knn_vector",
    "class": "solr.DenseVectorField",
    "vectorDimension": "768",
    "similarityFunction": "cosine"
  },
```

The model `all-mpnet-base-v2` generates a vector of 768 dimension.
So, the vectorDimension in this demo is 768.

4. Index documents

Upload the documents prepared to Solr and index.

```shell
sh ./index-data.sh
```

5. Vector search!

```shell
python3 vector_search.py
```

The python script asks you to input a query.
You can type like "What is the capital city of France?"

```shell
% python3 vector_search.py
Input ?
What is the capital city of France?
[
  {
    "id": "2",
    "text": "the capital city of france is paris"
  },
  {
    "id": "1",
    "text": "what is the capital city of australia?"
  },
  {
    "id": "5",
    "text": "the population of paris is 2 million"
  }
]
```

# Conclusions

Solr can return relevant documents using vector search.

Since the language model has (some) general knowledge, we can query with abbreviation and misspelling too.
It can find correct documents with "What is the capital city of U.K.?", "What is the capital city of the United Kingdom?" and "What is the population of New York?".
Also, it can return the correct document for more complex query like "What is the population of the capital of U.K.?".
But please note that it doesn't use the knowledge in the documents.


# Implementation details

Since the vector search request is a very long request due to a query vector, HTTP GET request to solr doesn't work due to the request size limit.
I had to use JSON API with HTTP POST.