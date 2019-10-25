#!/bin/bash -x


tag="3"
image="telegram-bot"
repository="itstepdockerhub.azurecr.io"

docker build -t maxchv/${image}:${tag} .
echo -n "Enter the password: "
docker login --username itstepdockerhub --password $1 ${repository}
docker tag maxchv/${image}:${tag} ${repository}/maxchv/${image}:${tag}
docker push ${repository}/maxchv/${image}:${tag}
