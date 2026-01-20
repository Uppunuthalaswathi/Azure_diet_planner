import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# ---------------- MySQL Connection ----------------
def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME"),
            port=3306,
            connection_timeout=5   # 🔥 VERY IMPORTANT
        )
    except Error as e:
        print("Database connection error:", e)
        return None

# ---------------- Health Check ----------------
@app.route("/", methods=["GET"])
def home():
    return "Diet Planner API is running ✅"

# ---------------- Get All Diets ----------------
@app.route("/allDiet", methods=["GET"])
def get_all_diet():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM diet_planner")
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ---------------- Get Diet by Query ----------------
@app.route("/diet", methods=["GET"])
def get_diet_by_query():
    diet_id = request.args.get("id")
    if not diet_id:
        return jsonify({"error": "id parameter is required"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM diet_planner WHERE id=%s", (diet_id,))
        data = cursor.fetchone()

        if data:
            return jsonify(data), 200
        return jsonify({"message": "Diet not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ---------------- Get Diet by Path ----------------
@app.route("/diet/<int:id>", methods=["GET"])
def get_diet_by_path(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM diet_planner WHERE id=%s", (id,))
        data = cursor.fetchone()

        if data:
            return jsonify(data), 200
        return jsonify({"message": "Diet not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ---------------- Add Diet ----------------
@app.route("/diet", methods=["POST"])
def add_diet():
    data = request.get_json()

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO diet_planner
        (meal_type, food_item, protein_g, carbohydrates_g, fats_g, vitamins,
         minerals, calories_kcal, quantity_g,
         suitable_for_diabetes, suitable_for_bp, suitable_for_heart,
         suitable_for_kidney, suitable_for_liver,
         suitable_for_obesity, suitable_for_anemia)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            data.get("meal_type"),
            data.get("food_item"),
            data.get("protein_g"),
            data.get("carbohydrates_g"),
            data.get("fats_g"),
            data.get("vitamins"),
            data.get("minerals"),
            data.get("calories_kcal"),
            data.get("quantity_g"),
            data.get("suitable_for_diabetes"),
            data.get("suitable_for_bp"),
            data.get("suitable_for_heart"),
            data.get("suitable_for_kidney"),
            data.get("suitable_for_liver"),
            data.get("suitable_for_obesity"),
            data.get("suitable_for_anemia")
        )

        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"message": "Diet added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ---------------- Update Diet ----------------
@app.route("/diet/<int:id>", methods=["PUT"])
def update_diet(id):
    data = request.get_json()

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        sql = """
        UPDATE diet_planner SET
        meal_type=%s, food_item=%s, protein_g=%s, carbohydrates_g=%s,
        fats_g=%s, vitamins=%s, minerals=%s, calories_kcal=%s,
        quantity_g=%s, suitable_for_diabetes=%s, suitable_for_bp=%s,
        suitable_for_heart=%s, suitable_for_kidney=%s,
        suitable_for_liver=%s, suitable_for_obesity=%s,
        suitable_for_anemia=%s
        WHERE id=%s
        """

        values = (
            data.get("meal_type"),
            data.get("food_item"),
            data.get("protein_g"),
            data.get("carbohydrates_g"),
            data.get("fats_g"),
            data.get("vitamins"),
            data.get("minerals"),
            data.get("calories_kcal"),
            data.get("quantity_g"),
            data.get("suitable_for_diabetes"),
            data.get("suitable_for_bp"),
            data.get("suitable_for_heart"),
            data.get("suitable_for_kidney"),
            data.get("suitable_for_liver"),
            data.get("suitable_for_obesity"),
            data.get("suitable_for_anemia"),
            id
        )

        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"message": "Diet updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ---------------- Delete Diet ----------------
@app.route("/diet/<int:id>", methods=["DELETE"])
def delete_diet(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM diet_planner WHERE id=%s", (id,))
        conn.commit()
        return jsonify({"message": "Diet deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
