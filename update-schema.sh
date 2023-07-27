#!/bin/sh
curl -X POST 'http://localhost:8983/api/collections/vector_test/schema' -H 'Content-type: application/json' -d @schema.json
