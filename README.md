# WoWTCG-Tracker API

Python backend for WoWTCG Tracker app

#### Uses:

- [Poetry](https://python-poetry.org/) as an dependency manager
- [FastAPI](https://fastapi.tiangolo.com/) as an API framework
- [Prisma](https://www.prisma.io/) as an ORM

## Database

App should work with any database supported by Prisma. Currently development being done with assistance from [MariaDB](https://mariadb.org/).

## Setup

1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Install dependencies with `poetry install`
3. Setup DB with `poetry run task migrate`
- (Optional) Run development server with `poetry run task dev`
4. Run production server with `poetry run task prod`