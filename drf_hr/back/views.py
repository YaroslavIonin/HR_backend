from django.shortcuts import render
from .models import Resume


# Create your views here.
def proverca(request):
    resumes = Resume.objects.all()
    return render(request, 'resumes.html', {'resumes': resumes})
