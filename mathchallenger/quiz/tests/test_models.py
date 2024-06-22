import pytest
from django.contrib.auth.models import User
from ..models import Profile, QuesModel, Statistic, Leaderboard
from django.db.utils import IntegrityError  # exception for violating database integrity constraints


@pytest.mark.django_db
def test_create_profile():
    user = User.objects.create(username='testuser')
    profile = Profile.objects.create(user=user, user_type='student')

    assert profile.user == user
    assert profile.user_type == 'student'


@pytest.mark.django_db
def test_teacher_profile():
    user = User.objects.create(username='teacheruser1')
    profile = Profile.objects.create(user=user, user_type='teacher')

    assert profile.user == user
    assert profile.user_type == 'teacher'


@pytest.mark.django_db
def test_profile_string_representation():
    user = User.objects.create(username='teacheruser1')
    profile = Profile.objects.create(user=user, user_type='teacher')

    assert str(profile) == user.username + '\' profile'



@pytest.mark.django_db
def test_add_same_user():
    user = User.objects.create_user(username='james123', password='ABC12345+')

    with pytest.raises(IntegrityError):               # exception is being raised since we try to add the same user twice
        user2 = User.objects.create_user(username='james123', password='abc123ABC+')


@pytest.mark.django_db
def test_invalid_user():
    with pytest.raises(IntegrityError):               # exception is being raised since the user object doesn't have a value
        Profile.objects.create(user=None, user_type='student')



@pytest.mark.django_db
def test_question_string_representation():
    question = QuesModel.objects.create(
        question='What is 2+2?',
        op1='3',
        op2='4',
        op3='5',
        op4='6',
        ans='4',
        difficulty='beginner'
    )

    assert str(question) == 'What is 2+2?'



@pytest.mark.django_db
def test_question_attributes():
    question = QuesModel.objects.create(
        question='What is 2+2?',
        op1='3',
        op2='4',
        op3='5',
        op4='6',
        ans='4',
        difficulty='advanced'
    )

    assert question.op1 == '3'
    assert question.ans == '4'
    assert question.difficulty == 'advanced'



@pytest.mark.django_db
def test_question_filter():
    QuesModel.objects.create(
        question="What is 2 + 2?",
        op1="2",
        op2="3",
        op3="4",
        op4="5",
        ans="4",
        difficulty="beginner"
    )
    QuesModel.objects.create(
        question="What is 2 + 2?",
        op1="2",
        op2="3",
        op3="4",
        op4="5",
        ans="4",
        difficulty="advanced"
    )
    QuesModel.objects.create(
        question="What is 2 + 2?",
        op1="2",
        op2="3",
        op3="4",
        op4="5",
        ans="4",
        difficulty="medium"
    )
    questions = QuesModel.objects.filter(difficulty='beginner')

    assert questions.count() == 1



@pytest.mark.django_db
def test_get_question():
    wanted_question = QuesModel.objects.create(
        question="Which of following expressions are true?",
        op1="1+1=2",
        op2="3-2=5",
        op3="4-1=2",
        op4="5/2=2",
        ans="1+1=2",
        difficulty="medium"
    )
    different = QuesModel.objects.create(
        question="Which of following expressions are true?",
        op1="1+4=2",
        op2="3-1=5",
        op3="4-3=2",
        op4="4/2=2",
        ans="4/2=2",
        difficulty="beginner"
    )

    received_question = QuesModel.objects.get(pk=wanted_question.pk)        # retrieve the question by its primary key

    assert received_question == wanted_question

    with pytest.raises(AssertionError):                     # raising the exception AssertionError to make sure the two objects are not equal
        assert received_question == different



@pytest.mark.django_db
def test_delete_beginner_question():           # this test is for admin purposes since a normal user doesn't have the functionality to delete a question
    QuesModel.objects.create(
        question='What is 2+2?',
        op1='3',
        op2='4',
        op3='5',
        op4='6',
        ans='4',
        difficulty='beginner'
    )
    QuesModel.objects.create(
        question='What is 100*100?',
        op1='1000',
        op2='1000000',
        op3='10000',
        op4='100',
        ans='10000',
        difficulty='beginner'
    )
    QuesModel.objects.create(
        question='What is 12*49?',
        op1='467',
        op2='540',
        op3='532',
        op4='588',
        ans='588',
        difficulty='medium'
    )

    beginner_questions = QuesModel.objects.filter(difficulty='beginner')
    beginner_questions.delete()

    assert QuesModel.objects.filter(difficulty='beginner').count() == 0




@pytest.mark.django_db
def test_create_statistic_entry():
    user = User.objects.create(username='statuser')
    statistic = Statistic.objects.create(user=user, average=75, entries=4, difficulty='medium')

    assert statistic.user == user
    assert statistic.average == 75
    assert statistic.entries == 4
    assert statistic.difficulty == 'medium'






@pytest.mark.django_db
def test_statistic_update():
    user = User.objects.create_user(username='testuser', password='testpassword')
    statistic = Statistic.objects.create(
        user=user,
        average=75,
        entries=1,
        difficulty='beginner'
    )
    new_average = 85
    new_entries = 2
    statistic.average = new_average
    statistic.entries = new_entries
    statistic.save()
    updated_statistic = Statistic.objects.get(pk=statistic.pk)
    assert updated_statistic.average == new_average
    assert updated_statistic.entries == new_entries




@pytest.mark.django_db
def test_statistic_string_representation():
    user = User.objects.create_user(username='johnsmith', password='testpassword')
    statistic = Statistic.objects.create(
        user=user,
        average=75,
        entries=1,
        difficulty='beginner'
    )

    assert str(statistic) == 'johnsmith\' stats'





@pytest.mark.django_db
def test_statistic_delete():                    # this test only usable for admin purposes
    user = User.objects.create_user(username='testuser', password='testpassword')
    statistic = Statistic.objects.create(
        user=user,
        average=75,
        entries=1,
        difficulty='beginner'
    )
    statistic.delete()
    assert Statistic.objects.filter(user=user).count() == 0


@pytest.mark.django_db
def test_create_leaderboard_entry():
    user = User.objects.create(username='leaderuser')
    leaderboard = Leaderboard.objects.create(user=user, score=100, difficulty='medium')

    assert leaderboard.user == user
    assert leaderboard.score == 100
    assert leaderboard.difficulty == 'medium'



@pytest.mark.django_db
def test_leaderboard_string_representation():
    user = User.objects.create(username='jaden-smith')
    leaderboard = Leaderboard.objects.create(user=user, score=100, difficulty='medium')

    assert str(leaderboard) == 'jaden-smith\' scores'




@pytest.mark.django_db
def test_leaderboard_ordering():                # creating leaderboard entries, retrieving them ordered by their score attributes and checking the last and first entry
    user1 = User.objects.create(username='beginnerplayer')
    user2 = User.objects.create(username='champion123')
    user3 = User.objects.create(username='james123')

    Leaderboard.objects.create(user=user1, score=10, difficulty='advanced')
    Leaderboard.objects.create(user=user2, score=400, difficulty='advanced')
    Leaderboard.objects.create(user=user3, score=20, difficulty='advanced')

    scores = Leaderboard.objects.order_by('-score')      # '-' before score makes sure it is sorted in descending order
    assert scores.first().user.username == 'champion123'
    assert scores.last().user.username == 'beginnerplayer'


@pytest.mark.django_db
def test_leaderboard_filter_by_difficulty():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    Leaderboard.objects.create(user=user1, score=100, difficulty='medium')
    Leaderboard.objects.create(user=user2, score=200, difficulty='beginner')

    medium_scores = Leaderboard.objects.filter(difficulty='medium')
    beginner_scores = Leaderboard.objects.filter(difficulty='beginner')

    assert medium_scores.count() == 1
    assert beginner_scores.count() == 1



@pytest.mark.django_db
def test_update_leaderboard_score():
    user = User.objects.create(username='leader_user')
    leaderboard = Leaderboard.objects.create(user=user, score=100, difficulty='medium')

    new_score = 150
    leaderboard.score = new_score
    leaderboard.save()

    updated_leaderboard = Leaderboard.objects.get(pk=leaderboard.pk)
    assert updated_leaderboard.score == new_score



@pytest.mark.django_db
def test_delete_leaderboard_entry():
    user = User.objects.create(username='leader_user')           # this test only usable for admin purposes
    leaderboard = Leaderboard.objects.create(user=user, score=100, difficulty='medium')
    leaderboard.delete()

    assert Leaderboard.objects.filter(user=user).count() == 0
