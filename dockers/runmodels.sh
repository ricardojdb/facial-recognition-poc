#!/bin/bash

# If the docker image already exists don't build
if [[ "$(sudo docker images -q knn:latest 2> /dev/null)" != "" ]]
then
echo Image knn already built
else
sudo docker build -t knn knn/
fi

if [[ "$(sudo docker images -q vggface:latest 2> /dev/null)" != "" ]]
then
echo Image vggface already built
else
sudo docker build -t vggface vggface/ 
fi

# Run the vggface container locally
sudo docker run --runtime=nvidia --name=vggface-service --rm \
-dit -v C:\Users\rdiazbri\Documents\proyectos\facial-recognition\dockers\vggface:/app vggface

# Run the container in the port 7000
sudo docker run --name=knn-service --rm --link=vggface-service\
-dit -v C:\Users\rdiazbri\Documents\proyectos\facial-recognition\dockers\knn:/app -p 7000:7000 knn

