from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Test
from .models import Question
from .models import Answer
from .models import TestGroup

import re

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text', 'test')
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите вопрос'
                }
            ),
            'test': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        test_id = kwargs.pop('test_id', None)
        super(QuestionForm, self).__init__(*args, **kwargs)

        if test_id:
            self.initial['test'] = test_id

        answers = Answer.objects.filter(
            question=self.instance
        )

        self.delete_answer_id = []

        for answer in answers:
            input_name = 'answer_%s' % answer.pk
            if self.data and input_name not in self.data:
                self.delete_answer_id.append(answer.pk)
                continue

            checkbox_name = 'iscorrect_%s' % answer.pk
            self.fields[input_name] = forms.CharField(
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите ответ',
                })
            )
            self.fields[checkbox_name] = forms.BooleanField(
                required=False,
                widget=forms.CheckboxInput(attrs={
                    'value': 1
                })
            )

            self.initial[input_name] = answer.text
            self.initial[checkbox_name] = answer.is_correct

        self.create_new_field_from_post()

    def create_new_field_from_post(self):
        for field_name in self.data:
            if field_name not in self.fields:
                if field_name.startswith('newanswer_') and field_name != 'newanswer_':
                    num = re.split('_', field_name)[1]
                    self.fields[field_name] = forms.CharField(
                        widget=forms.TextInput(attrs={
                            'class': 'form-control',
                            'placeholder': 'Введите ответ'
                        })
                    )

                    checkbox_name = 'newiscorrect_%s' % num
                    self.fields[checkbox_name] = forms.BooleanField(
                        required=False,
                        widget=forms.CheckboxInput(attrs={
                              'value': 1
                        })
                    )

                    self.initial[field_name] = self.fields[field_name]
                    if self.fields[checkbox_name]:
                        self.initial[checkbox_name] = True

    def clean(self):
        answers = set()
        for field_name, answer in self.get_answers_cleaned_data():
            if answer not in answers:
                answers.add(answer)
            else:
                raise forms.ValidationError("Одинаковые ответы: %s" % answer)

        if not answers:
            raise forms.ValidationError("Не создано ни одного ответа")

        checkbox_values = [value for field_name, value in self.cleaned_data.items()
                           if (field_name.startswith('newiscorrect_') or field_name.startswith('iscorrect_'))
                           and field_name != 'newiscorrect_']

        if True not in checkbox_values:
            raise forms.ValidationError("Не выбрано ни одного правильного ответа")
        if False not in checkbox_values:
            raise forms.ValidationError("Все ответы выбраны как правильные")

    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit)

        for field_name in self.cleaned_data:
            if field_name.startswith('answer_'):
                answer_id = re.split('_', field_name)[1]
                Answer.objects.filter(pk=answer_id).update(
                    text=self.cleaned_data[field_name],
                    is_correct=self.cleaned_data['iscorrect_%s' % answer_id]
                )

            if field_name.startswith('newanswer_'):
                field_num = re.split('_', field_name)[1]
                Answer.objects.create(
                    question=question,
                    text=self.cleaned_data[field_name],
                    is_correct=self.cleaned_data['newiscorrect_%s' % field_num]
                )

        Answer.objects.filter(pk__in=self.delete_answer_id).delete()
        return question

    def get_answers_cleaned_data(self):
        for field_name in self.fields:
            if field_name.startswith('answer_') or field_name.startswith('newanswer_'):
                yield field_name, self.cleaned_data.get(field_name)

    def get_answer_fields(self):
        for field_name in self.fields:
            if field_name.startswith('answer_'):
                num = re.split('_', field_name)[1]
                yield self['iscorrect_' + num], self[field_name]
            if field_name.startswith('newanswer_'):
                num = re.split('_', field_name)[1]
                yield self['newiscorrect_' + num], self[field_name]


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('name', 'description', 'date_creation', 'test_group')

        labels = {
            'name': 'Название',
            'description': 'Описание',
            'date_creation': 'Дата создания',
            'test_group': 'Категории теста'
        }

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите название теста'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите описание'
                }
            ),
            'date_creation': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True
                }
            ),
            'test_group': forms.SelectMultiple(
                attrs={
                    'class': 'form-control'
                },
            )
        }

    def __init__(self, *args, **kwargs):
        testgroup_id = kwargs.pop('testgroup_id', None)
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['test_group'].required = False
        if testgroup_id:
            self.initial['test_group'] = testgroup_id


class TestGroupForm(forms.ModelForm):
    class Meta:
        model = TestGroup
        fields = ('name', 'description', 'date_creation')
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'date_creation': 'Дата создания'
        }

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите название категории'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите описание'
                }
            ),
            'date_creation': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True
                }
            )
        }


class SignupForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

