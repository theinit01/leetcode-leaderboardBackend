import requests

def prettify_user_data(user_data):
    prettified_data = {
        'Username': user_data['username'],
        'Accepted Submissions': {}
    }
    
    for submission in user_data['submitStats']['acSubmissionNum']:
        difficulty = submission['difficulty'].capitalize()
        prettified_data['Accepted Submissions'][difficulty] = submission['count']
    
    return prettified_data


def get_leetcode_user_data(username):
    url = 'https://leetcode.com/graphql'
    headers = {
        'Content-Type': 'application/json',
        #'Cookie': 'LEETCODE_SESSION=your_session_cookie',  # Replace with your session cookie
    }
    
    query = '''
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStats: submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    '''
    
    variables = {
        'username': username
    }
    
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    if 'errors' in data:
        raise Exception(f"Errors returned: {data['errors']}")
    
    return prettify_user_data(data['data']['matchedUser'])


if __name__ == '__main__':
    # for testing pusposes
    username = 'theinit01'
    user_data = get_leetcode_user_data(username)
    print(user_data)