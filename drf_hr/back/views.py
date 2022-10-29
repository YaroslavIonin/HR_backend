from rest_framework.response import Response
from .models import Resume, Vacancy
from .serializers import ResumeSerializer, VacancySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class IsOwnerFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(exp_work=request.user)


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_fields = ('exp_work', 'salary', 'department')
    ordering_fields = ['data_updated']
    search_fields = ['title', 'description']

    def create(self, request, *args, **kwargs):
        if not request.user.is_header_dep:
            return Response({'err': 'Создавать вакансии может только глава департамента'})
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, department=self.request.user.department)


class ResumeViewSet(ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_fields = ('exp_work', 'salary')
    ordering_fields = ['data_updated']
    search_fields = ['full_name']

    def get_queryset(self):
        if self.request.user.is_header_dep:
            return Resume.objects.all()
        return Resume.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if len(Resume.objects.filter(user=self.request.user.id)) != 0:
            return Response({'err': 'У сотрудника может быть только одно резюме.'})
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user.id != self.request.user.id:
            return Response({'err': 'Нельзя изменять чужое резюме'})
        status = self.request.data['status']
        file = self.request.data['file']
        exp_work = self.request.data['exp_work']
        salary = self.request.data['salary']
        print(type(status), type(file), type(exp_work), type(salary))
        err = []
        if status == 'Y_P':
            if exp_work is None:
               err.append('Стаж работы')
            if salary == '0':
               err.append('Желаемая заработная плата')
            if file == '':
               err.append('Файл с резюме')
        print(err)
        if len(err) > 0:
            e = 'Заполните поля: {}.'.format(', '.join(err))
            return Response({'err': e})
        else:
            return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
