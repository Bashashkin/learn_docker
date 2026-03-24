from flask import Flask, render_template
from data import generate_data
from analysis import analyze, plot_prices

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
