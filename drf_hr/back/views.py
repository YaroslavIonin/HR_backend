from django.db.models import Q
from rest_framework.response import Response
from .filters import VacancyFilter, ResumeFilter
from .models import Resume, Vacancy, Skills
from .serializers import ResumeSerializer, VacancySerializer, SkillsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly, IsHeaderOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import pagination
from rest_framework.views import APIView
from accounts.models import User
from rest_framework import generics


class VacancyViewSet(ModelViewSet):
    serializer_class = VacancySerializer
    permission_classes = (IsAuthorOrReadOnly, IsHeaderOrReadOnly)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = VacancyFilter
    ordering_fields = ['data_updated']
    search_fields = ['title', 'description']

    # pagination_class = PageNumberSetPagination

    def get_queryset(self):
        if 'status' in self.request.query_params:
            return Vacancy.objects.filter(user=str(self.request.user.id))
        return Vacancy.objects.filter(status=1)

    def create(self, request, *args, **kwargs):
        if not request.user.is_header_dep:
            return Response({'err': 'Создавать вакансии может только глава департамента'})
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, department=self.request.user.department)


class FavoriteVacancies(generics.GenericAPIView):
    queryset = Vacancy.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(id=self.request.user.id)
        favorite_vacancies = [
            VacancySerializer(
                Vacancy.objects.get(id=vacancy.id),
                context=self.get_serializer_context()).data
            for vacancy in user.favorite_vacancies.all()]
        return Response({
            'vacancies': favorite_vacancies
        })

    def put(self, request):
        user = User.objects.get(id=self.request.user.id)
        vacancy = Vacancy.objects.get(id=self.request.query_params['id'])
        if vacancy in user.favorite_vacancies.all():
            user.favorite_vacancies.remove(vacancy)
        else:
            user.favorite_vacancies.add(vacancy)
        return Response({
            'status': 'ok'
        })


class SimilarVacancies(generics.GenericAPIView):
    queryset = Vacancy.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_similar(self, id_v):
        vacancy = Vacancy.objects.get(id=id_v)
        dep = vacancy.department
        exp_work = vacancy.exp_work
        vacancies = Vacancy.objects.filter(~Q(id=id_v) & Q(status=1) & Q(department=dep))

        a, b = 0, 1
        if exp_work < 3:
            if exp_work >= 1:
                a, b = 1, 3
        elif exp_work < 6:
            a, b = 3, 6
        else:
            a, b = 6, 6

        if a == 0 and b == 1:
            return vacancies.filter(Q(exp_work__lte=b))[:3]
        if a == 6 == b:
            return vacancies.filter(Q(exp_work__gte=b))[:3]
        else:
            return vacancies.filter(Q(exp_work__range=(a, b)))[:3]

    def get(self, request):
        if 'id' in self.request.query_params:
            id = self.request.query_params['id']
            similar_vacancies = [
                VacancySerializer(
                    vacancy,
                    context=self.get_serializer_context()).data
                for vacancy in self.get_similar(id)]
            return Response({
                'vacancies': similar_vacancies
            })
        else:
            return Response({
                'error': 'Запрос должен содержать id вакансии в параметрах'
            })


class ResumeViewSet(ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = ResumeFilter
    ordering_fields = ['data_updated']
    search_fields = ['about_me']

    def get_queryset(self):
        if self.request.user.is_header_dep:
            if 'status' in self.request.query_params:
                return Resume.objects.filter(user=str(self.request.user.id))
            return Resume.objects.filter(status=1)
        return Resume.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if len(Resume.objects.filter(user=self.request.user.id)) != 0:
            return Response({'err': 'У сотрудника может быть только одно резюме.'})
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        data = request.data
        obj = self.get_object()
        if obj.user.id != self.request.user.id:
            return Response({'err': 'Нельзя изменять чужое резюме'})
        status = self.request.data['status']
        if 'salary' not in data:
            saved_resume = Resume.objects.get(id=data['id'])
            serializer = ResumeSerializer(instance=saved_resume, data={
                'status': status
            }, partial=True)
            if serializer.is_valid(raise_exception=True):
                saved_user = serializer.save()
                return Response({
                    'message': 'Данные успешно изменены!'
                })
        else:
            return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListSkills(APIView):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        skills = [SkillsSerializer(skill).data for skill in Skills.objects.all()]
        return Response({
            'skills': skills
        })

