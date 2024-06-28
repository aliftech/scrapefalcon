# ScrapeFalcon

## Installation

### Create a venv

```bash
py -m venv env
```

### Activate venv

```bash
.\env\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Setup Project

```bash
alembic init alembic
```

```bash
docker-compose -f docker-compose.yml up --build
```

```bash
docker-compose up -d
```

### Database Migration

```bash
alembic revision -m "create table_name table"
```

```bash
alembic upgrade head
```

```bash
alembic downgrade -1
```

### Running Backend Service

```bash
uvicorn main:app --reload
```
