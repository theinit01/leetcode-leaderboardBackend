from models import get_database_connection
from api import get_leetcode_user_data


def update_leetcode_data():
    '''
    Function to update user data in the database
    '''
    try:
        conn = get_database_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT username FROM user_submissions')
        rows = cursor.fetchall()

        for row in rows:
            try:
                username = row[0]
                user_data = get_leetcode_user_data(username)
            except:
                continue
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
