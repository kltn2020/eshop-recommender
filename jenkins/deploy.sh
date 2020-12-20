#!/bin/bash

docker rm -f eshop-recommender

docker run -d --name eshop-recommender \
  --network my-net \
  -p 5000:5000 \
  ${DOCKER_IMAGE}:$TAG
