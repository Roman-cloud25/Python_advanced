from django.http import HttpResponse

# Create your views here.
def hello_view(request):
    return HttpResponse("Hello, Roman")