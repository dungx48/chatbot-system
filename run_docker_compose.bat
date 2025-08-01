docker-compose -f cicd/docker-compose.yml down
docker-compose -f cicd/docker-compose.yml up --build
docker-compose restart mychatbot