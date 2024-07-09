import psycopg2

# Function to create a database and table
def create_database():
    conn = psycopg2.connect(
        host="ep-flat-block-a5w9o2vm.us-east-2.aws.neon.tech",
        dbname="leetcode",
        user="leetcode_owner",
        password="kMxY5DoHO7Np",
        sslmode="require"
    )
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
    conn = psycopg2.connect(
        host="ep-flat-block-a5w9o2vm.us-east-2.aws.neon.tech",
        dbname="leetcode",
        user="leetcode_owner",
        password="kMxY5DoHO7Np",
        sslmode="require"
    )
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

# Example usage:
if __name__ == "__main__":
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
    print("done")