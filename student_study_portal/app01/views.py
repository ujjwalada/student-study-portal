
from importlib.util import find_spec
from multiprocessing import context
from turtle import title
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect


from .forms import DashboardForm, HomeworkForm, NotesForm, TodoForm, regForm
from .models import Homework, Notes, Todo
# Create your views here.
from django.contrib import messages
#  we have to install youtube-search-python to work with youtube api

from youtubesearchpython import VideosSearch
# from youtube_search import YoutubeSearch

# install pip install requests to work with book api
import requests

# to work with wiki we have to install pip install wikipedia library
import wikipedia
#  kis kis cheez me login reqired hai
# uske liye login required atributes add kre using decorators

from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'dashboard/home.html', {})


@login_required
def notes(request):
    # agar method post hai toh database me likha hua cheez store krega

    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'],
                          description=request.POST['description'])
            notes.save()
        messages.success(
            request, f"Notes Added from {request.user.username} successfully")

    else:
        form = NotesForm()

    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)


# for deleting notes
@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

#  for detialview of notes


@login_required
def detail(request, detail_id):
    data = get_object_or_404(Notes, pk=detail_id)
    context = {
        "data": data
    }
    return render(request, "dashboard/notes_detail.html", context)


@login_required
def homwork(request):
    # ye form create karega

    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                desc=request.POST['desc'],
                due=request.POST['due'],
                is_finished=finished
            )
            homeworks.save()
            messages.success(
                request, f'HomeWork Added from {request.user.username}!!')
    else:
        form = HomeworkForm()

    notes = Homework.objects.filter(user=request.user)
    if len(notes) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {'notes': notes, 'homework_done': homework_done, 'form': form}
    return render(request, 'dashboard/homework.html', context)


@login_required
def update_homework(request, pk=None):
    homwork = Homework.objects.get(id=pk)
    if homwork.is_finished == True:
        homwork.is_finished = False
    else:
        homwork.is_finished = True

    homwork.save()
    return redirect('homework')


@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")


@login_required
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=2)

        result_list = []
        #
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardForm()

    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)


@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()

    else:
        form = TodoForm()

    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'todo': todo,
        'form': form,
        'todos_done': todos_done,
    }
    return render(request, 'dashboard/todo.html', context)


@login_required
def update_todo(request, pk=None):
    homwork = Todo.objects.get(id=pk)
    if homwork.is_finished == True:
        homwork.is_finished = False
    else:
        homwork.is_finished = True
    homwork.save()
    return redirect('todo')


@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


def book(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {

                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink')

            }
            result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm()

    context = {'form': form}
    return render(request, 'dashboard/books.html', context)


@login_required
def dict(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
        except:
            context = {
                'form': form,
                'input': ''
            }
        return render(request, 'dashboard/dictionary.html', context)

    else:
        form = DashboardForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/dictionary.html', context)


@login_required
def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary

        }
    else:
        form = DashboardForm()
        context = {
            'form': form
        }
    return render(request, 'dashboard/wiki.html', context)


def register(request):
    if request.method == 'POST':
        form = regForm(request.POST)
        if form.is_valid():
            form.save()
            userName = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {userName}!!!!")
            return redirect("login")
    else:
        form = regForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/register.html', context)
