docker cp config-repo.py fair_eva:/FAIR_eva/
docker cp config/repositories.txt fair_eva:/FAIR_eva/config/
docker exec -it fair_eva python3 /FAIR_eva/config-repo.py