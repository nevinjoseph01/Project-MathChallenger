# Project MathChallenger

Math Challenger is a web-based application that is designed to provide an engaging platform for students to improve their math skills through quizzes. It also allows teachers to add quiz content and view the statistics of the students. This project supports two user roles (students and teachers), question management (full access only by the admin user), leaderboards and also statistical insights for participants.


## Who is it for?

- **Students:** Can participate in quizzes and view their scores and rankings on the leaderboard.
- **Teachers:** Can add questions to the quizzes and also view participant statistics.

## Features

- User Authentication (Login/Register)
- 2 different user roles (Student/Teacher)
- Add quiz questions (Teacher)
- Overview of the participants for each quiz (Teacher)
- Play quizzes of various different difficulties (Student)
- Leaderboard to view the players with the highest scores

## Networking Features and Database Storage

- uses a client-server architecture with HTTP for user interaction, authentication, quiz participation, leaderboard and statistics updates.

- uses SQLite for storing user accounts and their profiles (teacher/student), quiz questions with answers, quiz statistics, and leaderboard rankings



## How to install this application?

- 1.)  Either download as a zip file or clone with the following command:
  ```bash
  git clone https://github.com/nevinjoseph01/Nevin_Assignment2.git
  ```
- 2.)  Once this repository is cloned or downloaded, create the virtual environment in the root directory i.e. 'Nevin_Assignment2-main':
  (note: if a venv appears to be active already after cloning the repo, use the command 'deactivate')
  ```bash
  python -m venv venv
  ```
- 3.)  Activate the virtual environment:
  - command for windows:
  ```bash
  venv\Scripts\activate
  ```
  - command for macOs or Linux
  ```bash
  source venv/bin/activate
  ```

- 4.) Install the requirements
  ```bash
  pip install -r requirements.txt
  ```
  
- 5.) Change to the directory where the manage.py file is ('mathchallenger') and create the database migrations
  ```bash
  cd mathchallenger
  ```
  ```bash
  python manage.py migrate
  ```

- 6.) Since there are no questions in the database at the moment, add the sample quiz questions from fixtures to the db:
  ```bash
  python manage.py loaddata questionsample.json
  ```

- 7.) Finally run the development server and visit 'http://127.0.0.1:8000/'
  
  

## Tests

- To run the tests (using pytest) navigate to the directory 'mathchallenger' (note that there is also a subfolder for the app called 'mathchallenger' which is not used here!) and use the command:

```bash
pytest
```

  
  

  
  
  


