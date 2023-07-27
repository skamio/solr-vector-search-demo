#!/bin/sh

curl -X POST http://localhost:8983/api/collections -H 'Content-Type: application/json' -d ' 
  "create": {
    "name": "vector_test",
    "numShards": 1
  } 
'
