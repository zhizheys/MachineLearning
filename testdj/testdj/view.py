from django.http import HttpResponse
from django.shortcuts import render
from . import aaa

def hello(request):
    #return HttpResponse("Hello world ! ")
    a = aaa.testA()
    context = {}
    context['hello'] = 'Hello Worldaa! ' + a.show()
    return render(request, 'hello.html', context)