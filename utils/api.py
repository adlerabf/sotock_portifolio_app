from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = "data/tickers.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Acessar por nome da coluna
    return conn

@app.route("/tickers", methods=["GET"])
def get_tickers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT tickers FROM tickers")
        rows = cursor.fetchall()
        conn.close()
        tickers = [row["tickers"] for row in rows] 
        return jsonify(tickers)
    except Exception as e:
        print(f"Erro ao acessar o banco: {e}")
        return jsonify({"error": "Could not fetch tickers from database."}), 500

if __name__ == "__main__":
    app.run(debug=True)


