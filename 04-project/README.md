# Лабораторная работа 4.1. Создание и развертывание полнофункционального приложения

## Вариант 5
- Бизнес-задача: CRM для малого бизнеса.
- Данные: Имя клиента, телефон, email, статус сделки.

## Цель работы
Применить полученные знания по созданию и развертыванию трехзвенного приложения (Frontend + Backend + Database) в кластере Kubernetes. 
Научиться организовывать взаимодействие между микросервисами.

## Задачи
- Бэкенд. Разработать API (FastAPI/Flask), которое выполняет CRUD-операции с базой данных.
- Фронтенд. Разработать интерфейс (Streamlit), который обращается к API и отображает данные (таблицы/графики).
- Docker. Написать Dockerfile для обоих сервисов, собрать образы и (опционально) загрузить их в Docker Hub или использовать локально.
- Kubernetes. Написать манифесты (Deployment, Service) для БД, Бэкенда и Фронтенда.
- Развертывание. Запустить приложение в кластере и проверить сквозную работу (БД <-> Бэк <-> Фронт).

## Стек
- PostgreSQL 13
- FastAPI
- Streamlit
- Docker
- Kubernetes

## Ход работы

Структура проекта

<img width="295" height="357" alt="image" src="https://github.com/user-attachments/assets/b934533d-753f-4338-9e75-70412f7e4a73" />

backend/main.py
```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "API is working"}

@app.get("/clients")
def get_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()

@app.post("/clients")
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
```

backend/schemas.py
```python
from pydantic import BaseModel

class ClientCreate(BaseModel):
    name: str
    phone: str
    email: str
    status: str
```

backend/database.py
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL")

# ждём пока поднимется postgres
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        conn = engine.connect()
        conn.close()
        break
    except Exception:
        print("DB not ready, retrying...")
        time.sleep(3)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

backend/models.py
```python
from sqlalchemy import Column, Integer, String
from database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    status = Column(String)
```

backend/Dockerfile
```Dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

frontend/app.py
```python
import streamlit as st
import requests

API_URL = "http://backend-service:8000"

st.title("Client Registry CRM")

# Добавление клиента
st.header("Добавить клиента")
name = st.text_input("Имя")
phone = st.text_input("Телефон")
email = st.text_input("Email")
status = st.selectbox("Статус", ["new", "in_progress", "closed"])

if st.button("Добавить"):
    requests.post(f"{API_URL}/clients", json={
        "name": name,
        "phone": phone,
        "email": email,
        "status": status
    })

# Отображение
st.header("Список клиентов")
data = requests.get(f"{API_URL}/clients").json()
st.table(data)
```

frontend/Dockerfile
```Dockerfile
FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
k8s/backend-deployment.yaml
```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: leshadocker/backend
        env:
        - name: DATABASE_URL
          value: postgresql://user:password@postgres:5432/clients
        ports:
        - containerPort: 8000
```

k8s/frontend-deployment.yaml
```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: leshadocker/frontend
        ports:
        - containerPort: 8501
```

k8s/postgres-deployment.yaml
```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:14
        env:
        - name: POSTGRES_DB
          value: clients
        - name: POSTGRES_USER
          value: user
        - name: POSTGRES_PASSWORD
          value: password
        ports:
        - containerPort: 5432
```

k8s/services.yaml
```YAML
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  selector:
    app: postgres
  ports:
    - port: 5432

---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
    - port: 8000
  type: ClusterIP

---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: frontend
  ports:
    - port: 8501
  type: NodePort
```

Сборка образа

<img width="916" height="359" alt="image" src="https://github.com/user-attachments/assets/35df78cc-76c8-471a-ad52-aafe3bb5d914" />

Запуск

<img width="399" height="120" alt="image" src="https://github.com/user-attachments/assets/66dd16e5-e7ef-4866-b4ac-7fe286eef1a1" />

Информация о подах

<img width="715" height="163" alt="image" src="https://github.com/user-attachments/assets/e6d865c6-5bd7-44af-ada0-3d3246247914" />

Информация о сервисах

<img width="804" height="144" alt="image" src="https://github.com/user-attachments/assets/1a12fab7-3321-42ce-b74d-4ca0530ec110" />

Интерфейс приложения
<img width="1193" height="653" alt="image" src="https://github.com/user-attachments/assets/6a387113-5d16-44ad-850e-75793a3e97dc" />

Ввод клиента
<img width="1166" height="582" alt="image" src="https://github.com/user-attachments/assets/4445724a-a758-4ea5-aba8-823f6f3c7625" />

Вывод информации о клиентах
<img width="1162" height="652" alt="image" src="https://github.com/user-attachments/assets/de38a520-3ba2-4497-be61-9e543276cca8" />

## Вывод

В ходе лабораторной работы было создано приложение-CRM для малого бизнеса. Бекенд реализован на FastAPI, подключение к PostgreSQL через SQLAlchemy. Фронтенд - на Streamlit. Все контейнеризировано и под управлением Kubernetes.
