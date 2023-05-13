#!/bin/bash
docker run \
-d \
-p 80:80 \
--restart always \
--network manager \
--volume "$(pwd)":/book-manager \
--name book-manager book-manager
docker logs -f book-manager


