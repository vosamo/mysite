# coding:utf-8
from django.shortcuts import render, get_object_or_404
from django.template import Context,loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
from .models import Question, Choice

# def index(request):
#     latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
#     return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})
#
# def detail(request,question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

#通用视图重写上面三个方法
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 重新显示投票表单页面
        return render(request, 'polls/detail.html',{
            'question':p,
            'error_message': "You didn't select a choice!",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

# 简要说明：
# (1)request.POST是一个类字典对象，让你可以通过关键字的名字获取提交的数据。本例子中，requset.POST['choice']以字符串的形式返回选择的Choice
# 的id。
# (2)如果POST数据中没有提供choice，request.POST['choice']将引发一个KeyError。上面的代码检查KeyError，如果没有给出choice，将重新显示Question表单和错误信息。
# (3)最后返回HttpResponseRedirect，将用户重定向到results页面。
# (4)reverse函数避免了我们在视图函数中使用硬编码URL。
