from rest_framework.response import Response
from .models import Resume, Vacancy
from .serializers import ResumeSerializer, VacancySerializer
from rest_framework.viewsets import ModelViewSet


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.user.is_header_dep:
            return Response({'err': 'Создавать вакансии может только глава департамента'})
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, department=self.request.user.department)


class ResumeViewSet(ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def create(self, request, *args, **kwargs):
        if len(Resume.objects.filter(user=self.request.user.id)) != 0:
            return Response({'err': 'У сотрудника может быть только одно резюме.'})
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
