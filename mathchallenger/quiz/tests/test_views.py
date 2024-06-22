import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from ..models import Profile, QuesModel, Leaderboard, Statistic

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def create_user():       # this fixture creates the user instance
    def user_instance(username, password, user_type):
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, user_type=user_type)          # every user needs to have a profile to use the application!
        return user
    return user_instance

@pytest.fixture          # these fixtures provide some test quiz data
def create_math_quiz_questions():
    beginner_questions = [
        QuesModel.objects.create(
            question='What is 2 + 2?',
            op1='3', op2='4', op3='5', op4='6', ans='4', difficulty='beginner'
        ),
        QuesModel.objects.create(
            question='What is 10 * 5?',
            op1='40', op2='50', op3='60', op4='70', ans='50', difficulty='beginner'
        ),
        QuesModel.objects.create(
            question='What is 100 / 10?',
            op1='10', op2='20', op3='30', op4='40', ans='10', difficulty='beginner'
        ),
        QuesModel.objects.create(
            question='What is 5 - 3?',
            op1='1', op2='2', op3='3', op4='4', ans='2', difficulty='beginner'
        ),
    ]
    return beginner_questions



@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('landing-page'))      # sending a GET request after retrieving the URL with the reverse function
    assert response.status_code == 200
    assert 'Welcome to MathChallenger!' in response.content.decode()      # after getting a response, we check the content of the page with its decoded response object



@pytest.mark.django_db
def test_register_view(client):
    response = client.get(reverse('register-page'))
    assert response.status_code == 200
    assert 'Sign up' in response.content.decode()



@pytest.mark.django_db
def test_register_view_post(client):
    response = client.post(reverse('register-page'), {
        'username': 'newuser',
        'password1': 'password123',
        'password2': 'password123',
        'user_type': 'student'
    })
    assert response.status_code == 200


@pytest.mark.django_db
def test_skills_view(client, create_user):                   # creates the user instance, logs in, and requests for the view to the skills page as a student (teacher can't access this page!)
    user = create_user('student1', 'password123', 'student')      # note that user_type has to be student here
    client.login(username='student1', password='password123')
    response = client.get(reverse('skills-page'))
    assert response.status_code == 200



@pytest.mark.django_db
def test_add_question_view(client, create_user):
    user = create_user('teacher1', 'password123', 'teacher')    # note that user_type has to be teacher here
    client.login(username='teacher1', password='password123')
    response = client.get(reverse('add-question'))
    assert response.status_code == 200
    assert 'Add Question' in response.content.decode()



@pytest.mark.django_db
def test_play_quiz_view(client, create_user):
    user = create_user('student1', 'password123', 'student')
    client.login(username='student1', password='password123')
    response = client.get(reverse('play-quiz'), {'skill': 'beginner'})
    assert response.status_code == 200
    assert 'Quiz Questions' in response.content.decode()



@pytest.mark.django_db
def test_leaderboard_view(client):
    response = client.get(reverse('leaderboard'))
    assert response.status_code == 200
    assert 'Leaderboard' in response.content.decode()



@pytest.mark.django_db
def test_teachersite_view(client, create_user):
    user = create_user('teacher1', 'password123', 'teacher')
    client.login(username='teacher1', password='password123')
    response = client.get(reverse('teachersite'))
    assert response.status_code == 200
    assert 'Welcome to the teacher dashboard!' in response.content.decode()




@pytest.mark.django_db
def test_participants_view(client, create_user):
    user = create_user('teacher1', 'password123', 'teacher')
    client.login(username='teacher1', password='password123')
    response = client.get(reverse('participants'))
    assert response.status_code == 200
    assert 'View Participants' in response.content.decode()



@pytest.mark.django_db
def test_leaderboard_view(client, create_user):

    user1 = create_user('user1', 'password123', 'student')
    user2 = create_user('user2', 'password123', 'student')

    Leaderboard.objects.create(user=user1, score=100, difficulty='beginner')
    Leaderboard.objects.create(user=user2, score=80, difficulty='beginner')

    response = client.get(reverse('leaderboard'))

    assert response.status_code == 200

    assert 'Leaderboard' in str(response.content)
    assert user1.username in str(response.content)  # Check if user1's username is in the leaderboard




@pytest.mark.django_db
def test_play_quiz_and_see_stats(client, create_user, create_math_quiz_questions):

    user = create_user('student', 'password123', 'student')
    client.login(username='student', password='password123')           # create user instance and log in

    quiz_url = reverse('play-quiz') + '?skill=beginner'                # URl after user selecting the difficulty button 'beginner'
    response_get = client.get(quiz_url)                                # user gets redirected to the quiz page with its url and its query parameter obtained from the previous page
    assert response_get.status_code == 200

    answers = {}                            # create a dic with questions and user's (correct) answers as key, value pairs
    for question in create_math_quiz_questions:
        answers[question.question] = question.ans


    submission = client.post(quiz_url, data=answers)
    assert submission.status_code == 200


    assert 'Final Score' in str(submission.content.decode())
    assert 'Correct answers: 4' in str(submission.content.decode())
    assert 'Wrong answers: 0' in str(submission.content.decode())
    assert 'Total questions: 4' in str(submission.content.decode())         # since the user submitted only correct answers, we check the response object with appropriate values

    with pytest.raises(AssertionError):
        assert 'Total questions: 20' in str(submission.content.decode())    # since the fixtures only have 4 and not 20 questions, this should raise the exception AssertionError
