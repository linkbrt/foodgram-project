from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def index(request):
    print(1234)
    return render(request, template_name='../indexNotAuth.html')