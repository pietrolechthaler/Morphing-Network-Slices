mn -c
docker kill $(docker ps -a -q)
docker rm $(docker ps -a -q)
clear
