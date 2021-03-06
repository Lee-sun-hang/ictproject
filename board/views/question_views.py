from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

from django.db import connection

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('board:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'board/question_form.html', context)



@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # 수정일시 저장
            # question.save()
            ################ 취약한 코드 작성 ################
            author = question.author
            subject = question.subject
            content = question.content
            modify_date = timezone.now()
            cur = connection.cursor()
            subject, content = processString(subject, content)
            subject, content = xss_word_replace(subject, content)
            q = 'UPDATE ictproject.board_question set subject="{0}",content="{1}",\
             modify_date="{2}" WHERE id = {3};'.format(subject, content, modify_date, question_id)
            data = cur.execute(q)
            ################################################
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'board/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('board:detail', question_id=question.id)
    question.delete()
    return redirect('board:index')

def processString(str1, str2):
    specialChars = "'\"\\-#()@;=*/+"
    for specialChar in specialChars:
        str1 = str1.replace(specialChar, '')
        str2 = str2.replace(specialChar, '')
    str1 = str1.replace(',', ' ')
    str2 = str2.replace(',', ' ')
    return str1, str2

def xss_word_replace(str1, str2):
    str1 = str1.replace('<', '&lt;').replace('>', '&gt;')
    str2 = str2.replace('<', '&lt;').replace('>', '&gt;')
    return str1, str2