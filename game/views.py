from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Performance
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from lorem_text import lorem
from faker import Faker
from datetime import datetime
from distance import levenshtein


def get_random_text():
    faker = Faker()
    return faker.sentence()

@login_required
def home(request):
    performances = Performance.objects.filter(user=request.user).order_by('-date')
    context = {'performances': performances}
    return render(request, 'home.html', context)

@login_required
def game(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        typed_text = request.POST.get('typed_text')
        start_time = request.POST.get('start_time')
        end_time = datetime.now().timestamp()
        total_time_in_seconds = end_time - float(start_time)
        total_time_in_minutes = total_time_in_seconds / 60.0
        total_characters_typed = len(typed_text.strip())
        total_words_typed = total_characters_typed / 5.0

        distance = levenshtein(text, typed_text)
        accuracy_percentage = round((1 - distance / len(text)) * 100, 2)
        # correct_characters = 0
        # for i in range(len(typed_text)):
        #     if typed_text[i] == text[i]:
        #         correct_characters += 1
        # accuracy_percentage = (correct_characters / len(text)) * 100
        wpm = total_words_typed / total_time_in_minutes

        Performance.objects.create(user=request.user, text=text, typed_text=typed_text,
                                    accuracy=round(accuracy_percentage, 2), wpm=round(wpm, 2))

        return redirect('result', accuracy=accuracy_percentage, wpm=round(wpm, 2))

    else:
        text = get_random_text()
        return render(request, 'game.html', {'text': text, 'start_time': datetime.now().timestamp()})

@login_required
def save_performance(request):
    speed = request.POST['speed']
    accuracy = request.POST['accuracy']
    performance = Performance(user=request.user, speed=speed, accuracy=accuracy)
    performance.save()
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def result_view(request, accuracy, wpm):
    return render(request, 'result.html', {'accuracy': str(accuracy), 'wpm': str(wpm)})

