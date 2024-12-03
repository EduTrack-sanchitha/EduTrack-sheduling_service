from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "port": "8889",
    "user": "root",
    "password": "root",
    "database": "edutrack"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedules', methods=['GET'])
def get_schedules():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM schedules")
    schedules = cursor.fetchall()
    connection.close()
    return jsonify(schedules)

@app.route('/schedules', methods=['POST'])
def add_schedule():
    data = request.json
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO schedules (class_name, teacher, room, time) VALUES (%s, %s, %s, %s)",
                   (data["class_name"], data["teacher"], data["room"], data["time"]))
    connection.commit()
    connection.close()
    return jsonify({"message": "Schedule added successfully!"}), 201

@app.route('/schedules/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    data = request.json
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE schedules 
        SET class_name = %s, teacher = %s, room = %s, time = %s 
        WHERE id = %s
    """, (data["class_name"], data["teacher"], data["room"], data["time"], schedule_id))
    connection.commit()
    connection.close()
    return jsonify({"message": "Schedule updated successfully!"})

@app.route('/schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM schedules WHERE id = %s", (schedule_id,))
    connection.commit()
    connection.close()
    return jsonify({"message": "Schedule deleted successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
