#!/bin/bash
docker exec -it bookmanager-book-manager-1 celery -A config  worker -l INFO