#!/bin/bash

# If the docker image already exists don't build
if [[ "$(sudo docker images -q knn:latest 2> /dev/null)" != "" ]]
then
echo Image knn already built
else
sudo docker build -t knn knn/
fi

if [[ "$(sudo docker images -q vggface:gpu 2> /dev/null)" != "" ]]
then
echo Image vggface already built
else
sudo docker build -t vggface vggface/ 
fi

# Run the vggface container locally
sudo docker run --name=vggface-service --runtime=nvidia --rm \
-dit -v /home/deepai/Documents/projects/facial-recognition-poc/dockers/vggface:/app -p 7001:7000 vggface

# Run the container in the port 7000
sudo docker run --name=knn-service --link=vggface-service --rm  \
-dit -v /home/deepai/Documents/projects/facial-recognition-poc/dockers/knn:/app -p 7000:7000 knn

