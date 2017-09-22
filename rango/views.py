from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # A dictionary to pass to the template engine as its content
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # A dictionary to pass my name to the template engine as its content
    name_dict = {'my_name': "TonyVEVO"}
    return render (request, 'rango/about.html', context=name_dict)
