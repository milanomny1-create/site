from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__)
CSV_FILE = "index.csv"

# Read CSV into a list of dicts
def read_csv():
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Write list of dicts back to CSV
def write_csv(data):
    if data:
        headers = data[0].keys()
    else:
        headers = ["VEN", "NAME", "LOCATION"]
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

@app.route("/")
def home():
    return render_template("index.html")

# Search Column A (VEN) partially
@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    data = read_csv()
    results = [row for row in data if query in row["VEN"].lower()]
    return jsonify(results)

# Add new entry
@app.route("/add", methods=["POST"])
def add():
    new_entry = request.json  # {"VEN": "...", "NAME": "...", "LOCATION": "..."}
    data = read_csv()
    data.append(new_entry)
    write_csv(data)
    return {"status": "success", "entry": new_entry}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)