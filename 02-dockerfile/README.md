# Лабораторная работа 2.1. Создание Dockerfile и сборка образа

- ФИО: Башашкин А.М.
- Группа: АДЭУ-221
- Вариант: 5
- Предметная область: Недвижимость

## Цель работы
Научиться разрабатывать воспроизводимые аналитические инструменты.
Студенту необходимо пройти полный цикл: от написания Python-скрипта
для обработки бизнес-данных до его упаковки в Docker-образ и запуска в изолированной среде.

- Стек технологий: Flask Web
- Задание: Веб-приложение с HTML-шаблоном. При заходе на главную страницу отображает таблицу с данными (Pandas to HTML) по вашей тематике.

Структура приложения:

<img width="291" height="193" alt="image" src="https://github.com/user-attachments/assets/1029bf01-a2a8-46c0-b8fd-e34381b95f4e" />

Генерация данных:
```python
import pandas as pd
import random

def generate_data(n=100):
    districts = ["Центр", "Север", "Юг", "Запад", "Восток"]
    materials = ["Кирпич", "Панель", "Монолит"]

    data = []

    for _ in range(n):
        area = random.randint(20, 150)
        price = area * random.randint(80000, 200000)

        data.append({
            "Район": random.choice(districts),
            "Площадь": area,
            "Цена": price,
            "Этаж": random.randint(1, 25),
            "Год постройки": random.randint(1970, 2023),
            "Материал": random.choice(materials)
        })

    return pd.DataFrame(data)
```

Анализ данных и визуализация:

```python
import matplotlib.pyplot as plt

def analyze(df):
    df["Цена за м2"] = df["Цена"] / df["Площадь"]

    avg_price = df["Цена"].mean()
    avg_price_per_m2 = df["Цена за м2"].mean()

    by_district = df.groupby("Район")["Цена"].mean().reset_index()

    top_expensive = df.sort_values(by="Цена", ascending=False).head(5)

    return {
        "df": df,
        "avg_price": avg_price,
        "avg_price_per_m2": avg_price_per_m2,
        "by_district": by_district,
        "top_expensive": top_expensive
    }

def plot_prices(df):
    df.groupby("Район")["Цена"].mean().plot(kind="bar")
    plt.title("Средняя цена по районам")
    plt.xticks(rotation=30)
    plt.tight_layout()  
    plt.savefig("static/plot.png")
    plt.close()
```

Создание приложения:
```python
from flask import Flask, render_template
from data import generate_data
from analysis import analyze, plot_prices

app = Flask(name)

@app.route("/")
def index():
    df = generate_data(100)
    plot_prices(df)
    result = analyze(df)

    table_html = result["df"].to_html(classes="table table-striped", index=False)

    return render_template(
        "index.html",
        table=table_html,
        avg_price = int(result["avg_price"]),
        avg_price_per_m2 = int(result["avg_price_per_m2"])
    )

if name == "main":
    app.run(host="0.0.0.0", port=5000)
```

Dockerfile:

<img width="459" height="266" alt="image" src="https://github.com/user-attachments/assets/41d4409e-853e-4515-bd82-eb0a10d0fbd7" />

--no-cache-dir: отключает кэширование pip

requirements.txt:

<img width="129" height="71" alt="image" src="https://github.com/user-attachments/assets/2ade2970-633e-4a6d-a2ef-271569e6c1c1" />

Файл .dockerignore:

<img width="273" height="598" alt="image" src="https://github.com/user-attachments/assets/a423c963-fcf1-4bcb-a313-a7881b71d8b3" />

Сборка:

<img width="1009" height="344" alt="image" src="https://github.com/user-attachments/assets/c6caf3c0-c549-4263-b6ff-51a97b1cd661" />

Запуск контейнера:

<img width="1108" height="180" alt="image" src="https://github.com/user-attachments/assets/599c035f-30b4-44d3-8b09-33d94180034f" />


Приложение:
<img width="1189" height="612" alt="image" src="https://github.com/user-attachments/assets/1b0280f4-69b6-4c84-9cb5-ea939fc10d77" />

<img width="645" height="510" alt="image" src="https://github.com/user-attachments/assets/d2070f3d-c7b6-4163-8c54-81c8a65c50d3" />

## Вывод:
В ходе работы было создано веб-приложение внутри контейнера. Python использовался для генерации, визуализации и анализа данных, а также модуль Flask для веба.
