# Mevent

Welcome to Mevent, a streamlined platform designed to facilitate the organization and discovery of meetups. Dive into a world of events tailored to your interests and locality. 

## Prerequisites

Before diving into the setup, ensure you have the following installed:
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start

Follow these steps to get your Meetups App running in no time:

1. **Environment Setup**: Copy the `.env.example` file to `.env` in the root directory and fill it out with your specifics.
```bash
cp .env.example .env
```
2. **Launch Containers**: Run the following command to start your app.
```bash
docker-compose -f deployments/docker-compose.yml up -d
```
3. **Access App**: Open your browser and navigate to `http://localhost:8000/swagger` to see your app in action.

## Development Setup

For a more hands-on development environment with easier debugging:

1. Set up your `.env` file as described in the Quick Start section.
2. Start your Postgres database:
```bash
docker-compose -f deployments/docker-compose-db.yml up -d
```
3. Install geo dependencies:
   - Linux:
   ```bash
   sudo apt-get install binutils libproj-dev gdal-bin
   ```
   - Mac:
   ```bash
   brew install binutils proj gdal
   ```
4. Set up your virtual environment and install dependencies:
```bash
pip install -r requirements/local.txt
```
5. Install pre-commit hooks with:
```bash
pre-commit install
```
6. Apply database migrations:
```bash
python manage.py migrate
```
7. Start the server:
```bash
python manage.py runserver
```
8. Visit `http://localhost:8000/swagger` to verify it's running.



## Testing

Our tests are split into synchronous and asynchronous categories. Run them separately for the best results:

- Synchronous tests:
```bash
pytest -m "not asyncio"
```
- Asynchronous tests:
```bash
pytest -m asyncio
```

Feel free to explore, contribute, and help us make Mevent the go-to platform for discovering and organizing events!
