"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question,Choice,User
from django.template import loader
from django.core.urlresolvers import reverse
from app.forms import QuestionForm, ChoiceForm,UserForm
from django.shortcuts import redirect
import json


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Autor de la web',
            'message':'Datos de contacto',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def index(request):
    latest_question_list = None
    selected_subject = ""

    if request.method == "POST":
        selected_subject=request.POST['subject']
        latest_question_list = Question.objects.order_by('-pub_date').filter(subject__iexact=selected_subject)
    
    # preload all questions only for logged in users
    elif request.user.is_authenticated:
        latest_question_list = Question.objects.order_by('-pub_date')

    question_subjects = Question.objects.values('subject')

    template = loader.get_template('polls/index.html')
    context = {
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': latest_question_list,
                'question_subjects': question_subjects,
                'selected_subject': selected_subject,
              }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
     question = get_object_or_404(Question, pk=question_id)
     return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:','question': question})

def question_choices(request, question_id):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    question = get_object_or_404(Question, pk=question_id)
    
    return render(request, 'polls/question_choices.html', {'title':'Respuestas asociadas a la pregunta:','question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    hasAnswered = False

    if 'is_correct_answer' in request.GET:
        hasAnswered = True
        isCorrect = request.GET['is_correct_answer'] == 'True'

    return render(request, 'polls/results.html', {
        'title':'Resultados de la pregunta:',
        'question': question,
        'hasAnswered': hasAnswered,
        'isCorrect': isCorrect,
    })

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    choice = request.POST['choice']
    try:
        selected_choice = p.choice_set.get(pk=choice)
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        correct_choice = p.choice_set.all()[p.correct_choice - 1]
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form. Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        return HttpResponseRedirect(reverse('results', args=(p.id,)) + "?is_correct_answer=" + str(correct_choice.id == int(choice)))

def question_new(request):
        message = ""
        if request.method == "POST":
            form = QuestionForm(request.POST)
            
            minNumChoices = 2
            maxNumChoices = 4
            validNumChoices = int(request.POST["num_choices"]) >= minNumChoices and int(request.POST["num_choices"]) <= maxNumChoices
            validCorrectChoice = int(request.POST["correct_choice"]) >= 1 and int(request.POST["correct_choice"]) <= int(request.POST["num_choices"])

            if not validNumChoices:
                message = "El n??mero de respuestas debe ser entre " + str(minNumChoices) + " y " + str(maxNumChoices)
            elif not validCorrectChoice:
                message = "El n??mero de la respuesta correcta debe estar entre 1 y " + request.POST["num_choices"]
            elif form.is_valid():
                question = form.save(commit=False)
                question.pub_date=datetime.now()
                question.save()
                message = "Pregunta a??adida!"
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = QuestionForm()

        return render(request, 'polls/question_new.html', {'form': form, 'message': message})

def choice_add(request, question_id):
        form = ChoiceForm()
        message = ""

        question = Question.objects.get(id = question_id)
        numChoices = Choice.objects.filter(question = question_id).count()

        if numChoices >= question.num_choices:
            message = "Se han insertado el n??mero m??ximo de respuestas posibles"
            form = None

        elif request.method =='POST':
            form = ChoiceForm(request.POST)
            if form.is_valid():
                choice = form.save(commit = False)
                choice.question = question
                choice.vote = 0
                choice.save()
                message = "Respuesta a??adida!"
                #form.save()
        #return render_to_response ('choice_new.html', {'form': form, 'poll_id': poll_id,}, context_instance = RequestContext(request),)
        return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ question.question_text,'form': form, 'message': message})

def chart(request, question_id):
    q=Question.objects.get(id = question_id)
    qs = Choice.objects.filter(question=q)
    dates = [obj.choice_text for obj in qs]
    counts = [obj.votes for obj in qs]
    context = {
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
    }

    return render(request, 'polls/grafico.html', context)

def user_new(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = UserForm()
        return render(request, 'polls/user_new.html', {'form': form})

def users_detail(request):
    latest_user_list = User.objects.order_by('email')
    template = loader.get_template('polls/users.html')
    context = {
                'title':'Lista de usuarios',
                'latest_user_list': latest_user_list,
              }
    return render(request, 'polls/users.html', context)