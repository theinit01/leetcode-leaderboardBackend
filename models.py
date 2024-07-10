import psycopg2
import os

# Database connection parameters
db_params = {
    'host': os.environ.get('HOST'),
    'dbname': os.environ.get('DBNAME'),
    'user': os.environ.get('USER'),
    'password': os.environ.get('PASSWD'),
    'sslmode': "require"
}

# Function to establish a database connection
def get_database_connection():
    conn = psycopg2.connect(**db_params)
    return conn

# Function to create a database and table
def create_database():
    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_submissions (
        username TEXT PRIMARY KEY,
        easy INTEGER,
        medium INTEGER,
        hard INTEGER,
        total INTEGER
    )
    ''')

    conn.commit()
    conn.close()

# Function to insert user data into the database
def insert_user_data(user_data):
    conn = get_database_connection()
    cursor = conn.cursor()

    username = user_data['Username']
    easy = user_data['Accepted Submissions'].get('Easy', 0)
    medium = user_data['Accepted Submissions'].get('Medium', 0)
    hard = user_data['Accepted Submissions'].get('Hard', 0)
    total = user_data['Accepted Submissions'].get('All', 0)

    cursor.execute('''
    INSERT INTO user_submissions (username, easy, medium, hard, total)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (username) DO UPDATE 
    SET easy = EXCLUDED.easy, medium = EXCLUDED.medium, hard = EXCLUDED.hard, total = EXCLUDED.total;
    ''', (username, easy, medium, hard, total))

    conn.commit()
    conn.close()

# Function to fetch all user data from the database
def get_all_user_data():
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
    return data

# Example usage:
if __name__ == "__main__":

    # just for testing purposes
    # Create the database and table if they don't exist
    create_database()

    # Example user data
    example_user_data = {
        'Username': 'example_user',
        'Accepted Submissions': {
            'Easy': 10,
            'Medium': 5,
            'Hard': 2,
            'All': 17
        }
    }

    # Insert example user data into the database
    insert_user_data(example_user_data)

    # Fetch all user data and print
    all_user_data = get_all_user_data()
    print(all_user_data)
