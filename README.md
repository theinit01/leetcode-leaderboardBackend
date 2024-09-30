
# LeetCode Leaderboard

This project is a web application to track and display the performance of users on LeetCode. It includes features such as adding users, displaying a leaderboard, and viewing individual user profiles.

## Features

- **Leaderboard**: Display a ranked list of users based on their LeetCode performance.
- **Add User**: Add new users to the leaderboard by entering their LeetCode username.
- **User Profiles**: View individual user profiles with a summary of their total questions solved.
- **Responsive Design**: The application is fully responsive and works well on different screen sizes.

## Technologies Used

- **Frontend**: React, React Router, Bootstrap
- **Backend**: Flask, PostgreSQL
- **Styling**: Custom CSS, Bootstrap

## Getting Started

### Prerequisites

- Node.js and npm installed on your machine.
- Python and pip installed on your machine.

### Installation

1. **Install frontend dependencies**:
    ```sh
    git clone https://github.com/theinit01/leetcode-leaderboard-frontend.git
    cd leetcode-leaderboard-frontend
    npm install
    ```

2. **Install backend dependencies**:
    ```sh
    git clone https://github.com/theinit01/leetcode-leaderboard-backend.git
    cd leetcode-leaderboard-backend
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the backend server**:
    ```sh
    cd leetcode-leaderboard-backend
    flask run
    ```

2. **Start the frontend development server**:
    ```sh
    cd cd leetcode-leaderboard-frontend
    npm start
    ```

### Configuration

- **Backend**: The backend is a Flask server that handles API requests for fetching and adding users.
- **Frontend**: The frontend is a React application that communicates with the backend server.

### Contributions
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes. 
Make commits to a new feature branch 

### License
This project is licensed under the MIT License. See the [LICENSE](LICENCE) file for details.
