from django.shortcuts import render
from .models import User


# Create your views here.
def proverca(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})
