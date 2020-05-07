docker rm $(docker stop $(docker ps -a -q));
docker-compose build --no-cache
docker-compose up -d