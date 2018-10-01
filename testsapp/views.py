from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib import auth
from django.http import JsonResponse

from .forms import TestForm
from .forms import QuestionForm
from .forms import TestGroupForm
from .forms import CustomAuthenticationForm
from .forms import SignupForm

from .models import Question
from .models import Test
from .models import TestGroup
from .models import Answer
from .models import UserResult

from django.contrib.auth.models import User
from django.views.generic import View

from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator

def home(request):
    test_groups = list(TestGroup.objects.all().values('pk', 'name', 'description'))
    test_without_group = Test.objects.filter(test_group__isnull=True).count()
    if test_without_group:
        test_groups.append({'pk': '',
                            'name': 'Без категории',
                            'description': 'Тесты, которые не отнесены ни к одной из существующих категорий'})
    return render(request, 'testsapp/home.html', {'test_groups': test_groups})


def show_tests(request, testgroup_id=None):
    if testgroup_id is None:
        tests = Test.objects.filter(test_group__isnull=True)
    else:
        testgroup_instance = TestGroupForm.Meta.model.objects.get(id=testgroup_id)
        tests = Test.objects.filter(test_group=testgroup_instance)

    tests_with_questions = Question.objects.filter(test__in=tests).values('test').distinct()
    clear_tests = Test.objects.filter(pk__in=tests_with_questions)
    return render(request, 'testsapp/show_tests.html', {'tests': clear_tests})


@user_passes_test(lambda u: u.is_superuser, login_url='permission_denied')
def add_question(request, test_id):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect('edit_test', test_id=question.test.pk)
    else:
        form = QuestionForm(test_id=test_id)
    return render(request, 'testsapp/edit_question.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser, login_url='permission_denied')
def edit_question(request, question_id):
    question_instance = QuestionForm.Meta.model.objects.get(pk=question_id)
    if request.method == "POST":
        edit_form = QuestionForm(request.POST, instance=question_instance)
        if edit_form.is_valid():
            question = edit_form.save()
            return redirect('edit_test', test_id=question.test.pk)
    else:
        edit_form = QuestionForm(instance=question_instance)
    return render(request, 'testsapp/edit_question.html', {'form': edit_form})


@user_passes_test(lambda u: u.is_superuser, login_url='permission_denied')
def delete_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    test_id = question.test.pk
    question.delete()
    return redirect('edit_test', test_id=test_id)


@user_passes_test(lambda u: u.is_superuser, login_url='permission_denied')
def add_test(request, testgroup_id):
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save()
            return redirect('edit_test', test_id=test.pk)
    else:
        form = TestForm(testgroup_id=testgroup_id)
    return render(request, 'testsapp/edit_test.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser, login_url='permission_denied')
def edit_test(request, test_id):
    test_instance = TestForm.Meta.model.objects.get(id=test_id)
    if request.method == 'POST':
        edit_form = TestForm(request.POST, instance=test_instance)
        if edit_form.is_valid():
            test = edit_form.save(commit=False)
            test.save()
            edit_form.save_m2m()
            messages.success(request, 'Тест успешно изменен')
            return redirect(edit_test, test.pk)
    else:
        edit_form = TestForm(instance=test_instance)
        questions = list(Question.objects.filter(test=test_id).values('pk', 'text'))
    return render(request, 'testsapp/edit_test.html',
                  {'form': edit_form, 'test_id': test_id, 'questions': questions})


@user_passes_test(lambda u: u.is_superuser, login_url='permission_denied')
def delete_test(request, test_id):
    test = Test.objects.get(pk=test_id)
    test.delete()
    return redirect('home')


@user_passes_test(lambda u: u.is_superuser, login_url='permission_denied')
def add_testgroup(request):
    if request.method == "POST":
        form = TestGroupForm(request.POST)
        if form.is_valid():
            testgroup = form.save()
            return redirect('edit_testgroup', testgroup_id=testgroup.pk)
    else:
        form = TestGroupForm()
    return render(request, 'testsapp/edit_testgroup.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser, login_url='permission_denied')
def edit_testgroup(request, testgroup_id):
    testgroup_instance = TestGroupForm.Meta.model.objects.get(id=testgroup_id)
    if request.method == 'POST':
        edit_form = TestGroupForm(request.POST, instance=testgroup_instance)
        if edit_form.is_valid():
            testgroup = edit_form.save()
            messages.success(request, 'Категория успешно изменена')
            return redirect('edit_testgroup', testgroup_id=testgroup.pk)
    else:
        tests = list(Test.objects.filter(test_group=testgroup_id).values('pk', 'name'))
        edit_form = TestGroupForm(instance=testgroup_instance)
    return render(request, 'testsapp/edit_testgroup.html',
                  {'form': edit_form, 'testgroup_id': testgroup_id, 'tests': tests})


@user_passes_test(lambda u: u.is_superuser, login_url='permission_denied')
def delete_testgroup(request, testgroup_id):
    testgroup = TestGroup.objects.get(pk=testgroup_id)
    testgroup.delete()
    return redirect('home')


def tests_without_group(request):
    tests = list(Test.objects.filter(test_group__isnull=True).values('pk', 'name'))
    return render(request, 'testsapp/tests_without_group.html', {'tests': tests})


def login_form(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm(None)
    return render(request, 'testsapp/login.html', {'form': form})


def signup_form(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('home')
    else:
        form = SignupForm(None)
    return render(request, 'testsapp/signup.html', {'form': form})


def logout_form(request):
    auth.logout(request)
    return redirect('home')


class UserQuestion(View):
    test_id = ''

    @method_decorator(lambda x: login_required(x, login_url='login'))
    def dispatch(self, *args, **kwargs):
        self.test_id = self.kwargs.get('test_id', None)
        return super(UserQuestion, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        next_question = self.next_question()
        if next_question:
            return render(request, 'testsapp/next_question.html',
                          {'test_id': self.test_id, 'question': next_question, 'answers': self.get_answers(next_question)})
        else:
            result_id = self.save_result()
            text_results = self.get_question_results()
            common_results = self.get_common_results()
            del request.session['test'][self.test_id]
            request.session.modified = True
            return render(request, 'testsapp/results.html',
                          {'result_id': result_id, 'text_results': text_results, 'common_results': common_results})

    def post(self, request, *args, **kwargs):
        question_id = request.POST['question_id']
        question_instance = Question.objects.get(id=question_id)
        answers = request.POST.getlist('answer')

        if not answers:
            messages.error(request, 'Не выбрано ни одного ответа')
        elif len(answers) == len(self.get_answers(question_instance)):
            messages.error(request, 'Все ответы не могут быть правильными')
        else:
            if request.session.get('test') is None:
                request.session['test'] = {}
            if request.session['test'].get(self.test_id) is None:
                request.session['test'][self.test_id] = {}

            request.session['test'][self.test_id].update({question_id: answers})
            request.session.modified = True
            return redirect('next_question', test_id=self.test_id)
        return render(request, 'testsapp/next_question.html',
                      {'test_id': test_id, 'question': question_instance, 'answers': self.get_answers(question_instance)})

    def next_question(self):
        if self.request.session.get('test') is None:
            first_question = Question.objects.filter(test=self.test_id).first()
            return first_question
        if self.request.session['test'].get(self.test_id) is None:
            self.request.session['test'][self.test_id] = {}

        old_questions = self.request.session['test'][self.test_id].keys()
        new_question = Question.objects.exclude(pk__in=old_questions).filter(test=self.test_id).first()
        return new_question

    @staticmethod
    def get_answers(question):
        answers = list(Answer.objects.filter(question=question))
        return answers

    def get_correct_answers(self):
        correct_answers = {}
        questions = Question.objects.filter(test=self.test_id)
        for question in questions:
            answers = list(Answer.objects.filter(question=question, is_correct = True).values('pk'))
            correct_answers.update({str(question.pk): [str(answer['pk']) for answer in answers]})
        return correct_answers

    def get_question_results(self):
        result = []
        questions = Question.objects.filter(test=self.test_id)
        correct_answers = self.get_correct_answers()
        user_answers = self.request.session['test'][self.test_id]
        user_correct_questions = [int(question) for question, answer in correct_answers.items() if
                                set(answer) == set(user_answers.get(question))]

        for question in questions:
            answers = Answer.objects.filter(question=question)
            answer_texts = dict((answer.pk, answer.text) for answer in answers)
            correct_answer_texts = [answer_texts.get(int(answer_id)) for answer_id in correct_answers.get(str(question.pk))]
            user_answer_texts = [answer_texts.get(int(answer_id)) for answer_id in user_answers.get(str(question.pk))]
            result.append({'question': question.text,
                           'correct_result': ','.join(correct_answer_texts),
                           'user_result': ','.join(user_answer_texts),
                           'is_correct': question.pk in user_correct_questions})
        return result

    def get_common_results(self):
        correct_answers = self.get_correct_answers()
        user_answers = self.request.session['test'][self.test_id]
        user_correct_questions = [int(question) for question, answer in correct_answers.items() if
                                  set(answer) == set(user_answers.get(question))]
        number_questions = Question.objects.filter(test=self.test_id).count()
        return {'number_correct_questions': len(user_correct_questions),
                'number_wrong_questions': (number_questions - len(user_correct_questions)),
                'percent': round((len(user_correct_questions)/number_questions)*100)}

    def save_result(self):
        user_answers = self.request.session['test'][self.test_id]
        correct_answers = self.get_correct_answers()
        test_instance = Test.objects.get(pk=self.test_id)

        user_correct_questions = [question for question, answer in correct_answers.items() if set(answer) == set(user_answers.get(question))]

        result = UserResult.objects.create(
            user = self.request.user,
            test = test_instance,
            number_correct_answers = len(user_correct_questions)
        )
        return result



