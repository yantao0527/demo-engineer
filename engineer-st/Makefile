include MakeEnv.mk
# include .env

agents-push-gcloud: agents-build registry-tag-agents registry-push-agents

####

install:
	python -m pip install -r requirements.txt

site:
	PYTHONPATH=../engineer-ai streamlit run Home.py

search:
	python scripts/search.py

demo:
	PYTHONPATH=../engineer-ai streamlit run pages/0_Demo_Engineer.py

docker-network:
	docker network create ai_agents

mysql-run:
	docker run --name mysql -d \
		--network ai_agents \
		-p 3306:3306 \
		-e MYSQL_ROOT_PASSWORD=admin123 \
		-v $(PWD)/setup/mysqlsampledatabase.sql:/docker-entrypoint-initdb.d/mysql.sql \
		mysql:8

mysql-rm:
	docker stop mysql
	docker rm mysql

mysql-cli:
	docker run -it --rm \
		--network ai_agents \
		-v $(PWD)/setup:/setup \
		mysql:8 \
		mysql -h mysql -u root -p

mysql-bash:
	docker run -it --rm \
		--network ai_agents \
		-v $(PWD)/setup:/setup \
		mysql:8 \
		bash

#### Build Docker Image ####

DOCKER_AGENTS=$(DOCKER_PREFIX)/$(IMAGE_NAME):$(IMAGE_VERSION)

agents-build:
	docker build -f setup/Dockerfile -t $(DOCKER_AGENTS) .

agents-rmi:
	docker rmi $(DOCKER_AGENTS)

agents-run:
	docker run --name ai_agents -d \
		--network ai_agents \
		-p 8501:8501 \
		-v $(PWD)/.env.docker:/app/.env \
		$(DOCKER_AGENTS)

agents-rm:
	docker stop ai_agents
	docker rm ai_agents

agents-push:
	docker push $(DOCKER_AGENTS)

DOCKER_MYSQL=$(DOCKER_PREFIX)/$(IMAGE_NAME_MYSQL):$(IMAGE_VERSION_MYSQL)

mysql-build:
	docker build -f setup/Dockerfile_mysql -t $(DOCKER_MYSQL) .

mysql-rmi:
	docker rmi $(DOCKER_MYSQL)

mysql-push:
	docker push $(DOCKER_MYSQL)

### Deploy Docker Container ####

stack-up:
	docker-compose -f setup/stack.yml --project-name stack up -d

stack-down:
	docker-compose -f setup/stack.yml --project-name stack  down

#### Build Gcloud Image ####

registry-enable:
	gcloud services enable artifactregistry.googleapis.com

registry-create:
	gcloud artifacts repositories create $(REPOSITORY_NAME) --repository-format=docker --location=$(LOCATION) --description="AI Agents Repository"

registry-auth:
	gcloud auth configure-docker $(LOCATION)-docker.pkg.dev

REGISTRY_MYSQL=$(REGISTRY_PREFIX)/$(IMAGE_NAME_MYSQL):$(IMAGE_VERSION_MYSQL)

registry-tag-mysql:
	docker tag $(DOCKER_MYSQL) $(REGISTRY_MYSQL)

registry-push-mysql:
	docker push $(REGISTRY_MYSQL)

DOCKER_ADMINER=adminer:latest
REGISTRY_ADMINER=$(REGISTRY_PREFIX)/adminer:latest

registry-tag-adminer:
	docker tag $(DOCKER_ADMINER) $(REGISTRY_ADMINER)

registry-push-adminer:
	docker push $(REGISTRY_ADMINER)

REGISTRY_AGENTS=$(REGISTRY_PREFIX)/$(IMAGE_NAME):$(IMAGE_VERSION)

registry-tag-agents:
	docker tag $(DOCKER_AGENTS) $(REGISTRY_AGENTS)

registry-push-agents:
	docker push $(REGISTRY_AGENTS)

#### Deploy gcloud run ####

gcloud-sql:
	gcloud sql instances create mysql --database-version=MYSQL_8_0 --tier=db-n1-standard-1 --region=$(LOCATION)

gcloud-classicmodels:
	gcloud sql databases create mysql --instance=classicmodels

gcloud-connection:
	gcloud sql instances describe mysql --format='value(connectionName)'

gcloud-sql-connect:
	gcloud run services update adminer --add-cloudsql-instances=ai-agents-386717:us-central1:mysql --region=$(LOCATION)

