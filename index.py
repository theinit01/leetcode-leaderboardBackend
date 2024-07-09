import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger, swag_from
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from api import get_leetcode_user_data
from models import insert_user_data, create_database

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)


SECRET_TOKEN = "secret"

def update_leetcode_data():
    '''
    Function to update user data in the database
    '''
    print('Job started...')
    try:
        conn = psycopg2.connect(
        host="ep-flat-block-a5w9o2vm.us-east-2.aws.neon.tech",
        dbname="leetcode",
        user="leetcode_owner",
        password="kMxY5DoHO7Np",
        sslmode="require"
    )
        cursor = conn.cursor()

        cursor.execute('SELECT username FROM user_submissions')
        rows = cursor.fetchall()

        for row in rows:
            username = row[0]
            user_data = get_leetcode_user_data(username)
            easy = user_data['Accepted Submissions'].get('Easy', 0)
            medium = user_data['Accepted Submissions'].get('Medium', 0)
            hard = user_data['Accepted Submissions'].get('Hard', 0)
            total = user_data['Accepted Submissions'].get('All', 0)
            cursor.execute(
                'UPDATE user_submissions SET easy = %s, medium = %s, hard = %s, total = %s WHERE username = %s',
                (easy, medium, hard, total, username))
            conn.commit()

        conn.close()
        print('Data updated successfully')
    except Exception as e:
        print(f'Error updating data: {e}')
      
    print('Job finished.')
def start_scheduler():
  # Scheduler configuration
  scheduler = BackgroundScheduler()
  ist_timezone = timezone('Asia/Kolkata')
  trigger = CronTrigger(hour=0, minute=0, timezone=ist_timezone)    # Run at midnight IST every day
  scheduler.add_job(update_leetcode_data, trigger)
  scheduler.start()

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
    conn = psycopg2.connect(
        host="ep-flat-block-a5w9o2vm.us-east-2.aws.neon.tech",
        dbname="leetcode",
        user="leetcode_owner",
        password="kMxY5DoHO7Np",
        sslmode="require"
    )
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
    req_data = request.get_json()
    username = req_data['username']
    token = request.headers.get('Authorization')

    if token != f"{SECRET_TOKEN}":
        return jsonify({'error': 'Unauthorized Access'}), 401

    try:
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
    conn = psycopg2.connect(
        host="ep-flat-block-a5w9o2vm.us-east-2.aws.neon.tech",
        dbname="leetcode",
        user="leetcode_owner",
        password="kMxY5DoHO7Np",
        sslmode="require"
    )
    cursor = conn.cursor()
    try:
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
      
    except psycopg2.Error as e:
      return jsonify({'msg': 'Use valid type - easy, meadium, hard, total'}), 500
    
    return jsonify(leaderboard_data)


if __name__ == '__main__':
    create_database()
    start_scheduler()
    app.run(host='0.0.0.0', debug=True)