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
