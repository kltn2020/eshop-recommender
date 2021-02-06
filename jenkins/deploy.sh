#!/bin/bash

docker rm -f eshop-recommender

docker run -d --name eshop-recommender \
  --network my-net \
  -e DB_HOST_IP=10.148.0.13 \
  -e DB_NAME=eshop \
  -e DB_USER_NAME=phathdt379 \
  -e DB_USER_PASS=password123 \
  -p 5000:5000 \
  ${DOCKER_IMAGE}:$TAG
