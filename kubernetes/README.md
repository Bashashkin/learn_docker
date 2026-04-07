# Лабораторная работа 3.1. Развертывание приложения в Kubernetes

## Вариант 5
Развернуть аналитическую БД ClickHouse и интерфейс Tabix (или использовать встроенный HTTP интерфейс) для выполнения SQL-запросов.


## Цель работы
Освоить процесс оркестрации контейнеров. Научиться разворачивать связки сервисов 
(аналитическое приложение + база данных/интерфейс) в кластере Kubernetes, управлять их масштабированием (Deployment)
и сетевой доступностью (Service).

## Задачи
- Создать манифест Deployment для основного аналитического приложения (согласно варианту).
- Создать манифест Deployment для вспомогательного сервиса (БД, кэш, GUI), если требуется по заданию.
- Создать манифесты Service для открытия доступа к приложениям.
- Запустить конфигурации в кластере и проверить взаимодействие компонентов.
- Оформить отчет в репозитории.

## Ход работы
Создание Deployment для Clickhouse
```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: clickhouse-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: clickhouse
  template:
    metadata:
      labels:
        app: clickhouse
    spec:
      containers:
        - name: clickhouse
          image: clickhouse/clickhouse-server:latest
          ports:
            - containerPort: 8123   # HTTP интерфейс
            - containerPort: 9000   # native client
```

Service для ClickHouse
```YAML
apiVersion: v1
kind: Service
metadata:
  name: clickhouse-service
spec:
  selector:
    app: clickhouse
  ports:
    - name: http
      protocol: TCP
      port: 8123
      targetPort: 8123
    - name: native
      protocol: TCP
      port: 9000
      targetPort: 9000
  type: ClusterIP
```

Deployment для Tabix
```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tabix-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: tabix
  template:
    metadata:
      labels:
        app: tabix
    spec:
      containers:
        - name: tabix
          image: spoonest/clickhouse-tabix-web-client
          ports:
            - containerPort: 80
```

Service для Tabix
```YAML
apiVersion: v1
kind: Service
metadata:
  name: tabix-service
spec:
  selector:
    app: tabix
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort
```

Запуск 

<img width="798" height="305" alt="image" src="https://github.com/user-attachments/assets/014fc82c-5014-4e5b-b9b2-85f1bce49e91" />

Создание подключения
<img width="1200" height="679" alt="image" src="https://github.com/user-attachments/assets/0f4365cb-055f-4578-85a7-f499eb513cbe" />


<img width="1187" height="573" alt="image" src="https://github.com/user-attachments/assets/14e965e8-1027-40b5-854a-1e57d6985ccc" />
<img width="1202" height="372" alt="image" src="https://github.com/user-attachments/assets/27ab959d-26f5-440e-9c71-08d372588d20" />

#Вывод

В ходе лабораторной работы было выполнено развертывание аналитического приложения в кластере Kubernetes. Были разработаны и применены манифесты Deployment для развертывания контейнеров ClickHouse и Tabix, для организации сетевого взаимодействия между компонентами были созданы Service-ресурсы

