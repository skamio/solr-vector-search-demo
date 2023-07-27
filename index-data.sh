#!/bin/bash
curl -X POST 'http://localhost:8983/api/collections/vector_test/update' -H 'Content-type: application/json' -d @docs.json
curl -X POST -H 'Content-type: application/json' -d '{"set-property":{"updateHandler.autoCommit.maxTime":15000}}' http://localhost:8983/api/collections/vector_test/config
