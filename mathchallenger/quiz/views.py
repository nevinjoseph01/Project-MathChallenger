# quiz\views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Profile,Leaderboard,QuesModel,Statistic
import random


def home(request):
    return render(request,'quiz/landingpage.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        usertype = request.POST.get('user_type')

        if usertype != 'student' and usertype != 'teacher':
            form.add_error(None,'Are you a student or a teacher?')          # when registering, either teacher or student option must be selected
        else:
            if form.is_valid():
                form.save()
                user = form.save()

                profile = Profile(user=user, user_type=usertype)           # after registering save the user and a user's profile with their profession
                profile.save()                                             # note: Only users with a profile can access specific quiz functionalities
                login(request, user)
                return redirect('landing-page')
    else:
        form = UserCreationForm()
    return render(request, 'quiz/register.html', {'form': form})



def skills(request):
    if request.user.profile.user_type == 'teacher':
        return redirect('teachersite')
    return render(request, 'quiz/skills.html')


def add_question(request):
    if request.user.profile.user_type != 'teacher':     # Only teachers can add questions
        return redirect('landing-page')

    error_message= []
    if request.method == 'POST':
        wrong_answer= False
        empty_field = False
        
        question=request.POST['question']
        op1=request.POST['op1']
        op2=request.POST['op2']
        op3=request.POST['op3']
        op4=request.POST['op4']
        ans=request.POST['ans']

        if ans not in [op1,op2,op3,op4]:
            wrong_answer = True                                # if teacher's answer doesn't match any options, display an error
        
        for field in [question,op1,op2,op3,op4]:
            if field == '':
                empty_field = True                             # if an empty field is entered, display an error
        
        if wrong_answer:
            error_message.append('Submitted answer must match an option!')
        if empty_field:
            error_message.append('Please enter values for all fields!')

        if len(error_message) == 0:
            question = QuesModel(
            question=request.POST['question'],
            op1=request.POST['op1'],
            op2=request.POST['op2'],
            op3=request.POST['op3'],
            op4=request.POST['op4'],
            ans=request.POST['ans'],
            difficulty=request.POST['difficulty']
            )
            question.save()
            return redirect('teachersite')   # if the question was entered successfully, save the question to the database

                
    return render(request, 'quiz/add_question.html', {'errors':error_message})



def play_quiz(request):
    if request.user.profile.user_type != 'student':
        return redirect('landing-page')

    skill = request.GET.get('skill')
    questions = list(QuesModel.objects.filter(difficulty=skill))          # After selecting difficulty, retrieve all questions for that difficulty in random order
    
    random.shuffle(questions)

    if request.method == 'POST':

        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            selected_answer = request.POST.get(q.question)

            if q.ans == selected_answer:
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = (score/total) * 10
        context = {
            'score': score,
            'percent': round(percent),
            'time': request.POST.get('timer', 0),               # retrieve the total time from the JS timer (return 0 if error happens)
            'correct': correct,
            'wrong': wrong,
            'total': total

        }
        stats = Leaderboard(user=request.user,score=score,difficulty=skill)
        stats.save()

        try:
            x = Statistic.objects.get(user=request.user,difficulty=skill)                                      # If the player has played the quiz before, retrieve the stats
        except Statistic.DoesNotExist:
            statistics = Statistic(user=request.user, average=percent, entries=1, difficulty= skill)           # If it's the player's first quiz, make a new Statistics object with entry set to 1
            statistics.save()
        else:
            x.average = (x.average + percent)//2                                                               # update the player's previous stats, if they played before
            x.entries += 1
            x.save()
        finally:
            return render(request, 'quiz/statistics.html', context)

    context = {'questions': questions, 'difficulty': skill}
    return render(request, 'quiz/play_quiz.html', context=context)




def leaderboard(request):
    scores = Leaderboard.objects.order_by('-score')                         # retrieve the Leaderboard scores in decreasing order
    return render(request, 'quiz/leaderboard.html', {'scores': scores})


def teachersite(request):
    return render(request,'quiz/teachersite.html')



def participants(request):                                      # show all quiz participants for each difficulty
    statistics = Statistic.objects.all()
    beginner_stats = statistics.filter(difficulty='beginner')
    medium_stats = statistics.filter(difficulty='medium')
    advanced_stats = statistics.filter(difficulty='advanced')
    human_calculator_stats = statistics.filter(difficulty='human_calculator')

    context = {
        'beginner_stats': beginner_stats,
        'medium_stats': medium_stats,
        'advanced_stats': advanced_stats,
        'human_calculator_stats': human_calculator_stats
    }

    return render(request, 'quiz/participants.html', context)
