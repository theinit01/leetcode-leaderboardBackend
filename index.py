import os
import psycopg2
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from flasgger import Swagger, swag_from
import random
import requests
import json
import datetime
from api import get_leetcode_user_data
from models import insert_user_data, create_database, get_database_connection
from cronapi.cron import update_leetcode_data

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)


# Load database IDs from JSON file
with open('database_ids.json') as f:
    DATABASE_IDS = json.load(f)['database_ids']

SECRET_TOKEN = "secret"


@app.route("/")
def index():
    return redirect('/health'), 302

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health Check Endpoint
    ---
    responses:
      200:
        description: Server is up and running
    """
    return jsonify({'status': 'ok'})

@app.route('/all_users', methods=['GET'])
@swag_from(methods=['GET'])
def get_all_data():
    """
    Route to fetch all user data from the database
    ---
    responses:
      200:
        description: Successful operation
        schema:
          type: array
          items:
            type: object
            properties:
              username:
                type: string
              easy:
                type: integer
              medium:
                type: integer
              hard:
                type: integer
              total:
                type: integer
    """
    try:
        conn = get_database_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM user_submissions')
        rows = cursor.fetchall()

        data = []
        for row in rows:
            data.append({
                'username': row[0],
                'easy': row[1],
                'medium': row[2],
                'hard': row[3],
                'total': row[4]
            })

        conn.close()

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_user', methods=['POST'])
@swag_from(methods=['POST'])
def add_data():
    """
    Route to fetch data for a username from LeetCode and add it to the database
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
      - name: Authorization
        in: header
        required: true
        type: string
    responses:
      200:
        description: Data added successfully
      401:
        description: Unauthorized
      500:
        description: Error adding data
    """
    try:
        req_data = request.get_json()
        username = req_data['username']
        token = request.headers.get('Authorization')

        if token != f"{SECRET_TOKEN}":
            return jsonify({'error': 'Unauthorized Access'}), 401

        user_data = get_leetcode_user_data(username)
        insert_user_data(user_data)
        
        return jsonify({'message': 'Data added successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/leaderboard/<type>', methods=['GET'])
@swag_from(methods=['GET'])
def get_leaderboard(type):
    """
    Route to fetch leaderboard based on total questions solved
    ---
    parameters:
      - name: type
        in: path
        required: true
        type: string
    responses:
      200:
        description: Successful operation
        schema:
          type: array
          items:
            type: object
            properties:
              username:
                type: string
              easy:
                type: integer
              medium:
                type: integer
              hard:
                type: integer
              total:
                type: integer
    """
    try:
        conn = get_database_connection()
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM user_submissions ORDER BY {type} DESC')
        rows = cursor.fetchall()

        leaderboard_data = []
        for row in rows:
            leaderboard_data.append({
                'username': row[0],
                'easy': row[1],
                'medium': row[2],
                'hard': row[3],
                'total': row[4]
            })

        conn.close()

        return jsonify(leaderboard_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/daily', methods=['GET'])
def get_random_problems():
    # Get the current date and use it as the seed
    today = datetime.date.today()
    seed = int(today.strftime('%Y%m%d'))
    random.seed(seed)

    problems = {'Algorithms': [], 'Database': []}

    # Fetch 2 random algorithm problems
    while len(problems['Algorithms']) < 2:
        random_id = random.randint(1, 3215)
        response = requests.get(f'https://lcid.cc/info/{random_id}')
        if response.status_code == 200:
            data = response.json()
            if data['categoryTitle'] == 'Algorithms' and not data['paidOnly']:
                problem_info = {
                    'title': data['title'],
                    'titleSlug': data['titleSlug']
                }
                if problem_info not in problems['Algorithms']:
                    problems['Algorithms'].append(problem_info)

    # Fetch 1 random database problem
    while len(problems['Database']) < 1:
        random_id = random.choice(DATABASE_IDS)
        response = requests.get(f'https://lcid.cc/info/{random_id}')
        if response.status_code == 200:
            data = response.json()
            if data['categoryTitle'] == 'Database' and not data['paidOnly']:
                problem_info = {
                    'title': data['title'],
                    'titleSlug': data['titleSlug']
                }
                if problem_info not in problems['Database']:
                    problems['Database'].append(problem_info)

    return jsonify(problems)

@app.route('/update', methods=['GET'])
def update_data():
    update_leetcode_data()
    return jsonify({'message': 'Data updated successfully'}), 200

if __name__ == '__main__':
    create_database()
    app.run(host='0.0.0.0', debug=True)