#!/usr/bin/env bash
set -e
TIMESTAMP=`date +%Y-%m-%d_%H-%M-%S`
BASE_IMAGE="private"
REGISTRY="mc2021rtl"
IMAGE="$REGISTRY/$BASE_IMAGE"
CID=$(docker ps | grep $IMAGE | awk '{print $1}')
docker pull $IMAGE
echo $TIMESTAMP
for im in $CID
do
    LATEST=`docker inspect --format "{{.Id}}" $IMAGE`
    RUNNING=`docker inspect --format "{{.Image}}" $im`
    NAME=`docker inspect --format '{{.Name}}' $im | sed "s/\///g"`
    echo "Latest:" $LATEST
    echo "Running:" $RUNNING
    echo "ID:" $CID
    if [ "$RUNNING" != "$LATEST" ];then
        echo "upgrading $NAME"
        docker stop $NAME
        docker rm -f $NAME
        docker rmi $RUNNING
        docker run -d --name="scraper" $IMAGE
        CID2=$(docker ps | grep $IMAGE | awk '{print $1}')
        echo "CID2: " $CID2
        docker cp ./database.ini $CID2:/app/database.ini
    else
        echo "$NAME up to date"
    fi
done
