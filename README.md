# START THE PROJECT

The project is using UV package manager. To start the project, you need to install the dependencies first. To do that, run the following command:

DOCKER commands:

compose command : docker compose build && docker compose up -d
image build : docker build -t vivpro-app .
run image : docker -d run -p 8080:80 vivpro-app

STEPS TO RUN THE PROJECT:

WITH DOCKER:

1. Just run the following command to start the project:

-- add the postgresql database details in the .env file

-- then run the following command:

`docker compose build && docker compose up -d`

WITHOUT DOCKER:

1. Install the dependencies by running the following command:

-- first install the uv package manager
`pip install uv`

-- then install the dependencies
`uv sync`

-- add the postgresql database details in the .env file

-- run the migrations
`uv run alembic upgrade head`

-- then run the project
`uvicorn app.main:app --reload` or `uv run fastapi dev`
