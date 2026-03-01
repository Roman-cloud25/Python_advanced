from django.http import HttpResponse

# Create your views here.
def hello_view(requst):
    return HttpResponse("Hello, Roman")