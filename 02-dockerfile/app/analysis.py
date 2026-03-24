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
