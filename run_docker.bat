docker build -f cicd/Dockerfile -t mychatbot .
docker run -d --name mychatbot_container -p 8000:8000 mychatbot