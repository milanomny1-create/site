from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)
CSV_FILE = "index.csv"

# Read CSV into a list of dictionaries
def read_csv():
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    data = read_csv()

    if query:
        # Filter rows where Col A contains the search query (case-insensitive)
        results = [row for row in data if query in row.get("Col A", "").lower()]
    else:
        results = data

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
