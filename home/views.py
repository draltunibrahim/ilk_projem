from django.shortcuts import render, HttpResponse

# Create your views here.
def home_view(request):
    if request.user.is_authenticated():
        context = {
            'isim' : 'ibrahim',
            'soyisim' : 'altun',
        }
    else:
        context = {
            'isim': 'misafir',
            'soyisim': '',
        }
    return render(request, 'home.html', context)