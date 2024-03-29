from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.mail import send_mass_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Department, Bid
from .serializers import UserAppSerializer, DepartmentSerializer, RegisterSerializer, RequestSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class DepartmentViewSet(ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (IsAuthenticated,)


class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserAppSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
        })


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('Такого пользователя не существует')
        if not user.check_password(password):
            raise AuthenticationFailed('Неверный пароль')

        return Response({
            "message": "Вход выполнен"
        })


class ProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAppSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            "user": UserAppSerializer(request.user, context=self.get_serializer_context()).data,
        })

    def put(self, request, *args, **kwargs):
        user = request.user
        if "full_name" in request.data:
            user.full_name = request.data["full_name"]
        if "phone_number" in request.data:
            user.phone_number = request.data["phone_number"]
        user.save()
        return Response({
            "user": UserAppSerializer(user, context=self.get_serializer_context()).data,
            "message": "Данные сохранены"
        })


class RequestView(ModelViewSet):
    serializer_class = RequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.query_params['status'] == '1':
            return Bid.objects.filter(addressee=self.request.user, status='1')
        elif self.request.query_params['status'] == '2':
            return Bid.objects.filter(addressee=self.request.user, status='2')

    def create(self, request, *args, **kwargs):
        from_email = settings.EMAIL_HOST_USER
        status = request.data['status']
        id_vr = request.data['id']
        destination = User.objects.get(id=int(request.data['destination']))
        bids = Bid.objects.filter(addressee=self.request.user, status=status, destination=destination, id_vr=id_vr)
        if len(bids) > 0:
            if status == '1':
                return Response({
                    'err': 'Вы уже отправили заявку на эту вакансию.'
                })
            else:
                return Response({
                    'err': 'Вы уже отправили заявку на это резюме.'
                })
        if 'title' in request.data:
            title = request.data['title']
        else:
            title = destination.full_name
        user = request.user
        full_name = user.full_name
        title_m = ''
        if status == '1':
            to_email_user = user.email
            to_email_header = destination.email
            message_to_header = f'Здравствуйте! На Вашу вакансию с названием "{title}" подал заявку сотрудник' \
                                f' {full_name}({to_email_user}), свяжитесь с ним по почте.'
            message_to_user = f'Здравствуйте, {full_name}! Вы подали заявку на вакансию с названием "{title}",' \
                              f' глава департамента этой вакансии свяжется с вами по почте.'
            title_m = f'Заявка на вакансию!'
        else:
            to_email_user = destination.email
            to_email_header = user.email
            message_to_header = f'Здравствуйте, {full_name}! Вы заинтересовались резюме сотрудника - {title}({to_email_user}), ' \
                                f'свяжитесь с ним по почте.'
            message_to_user = f'Здравствуйте, {title}! {full_name}({to_email_header}) - глава департамента "{user.department}" ' \
                              f'заинтересовался Вашем резюме, свяжитесь с ним по почте.'
            title_m = f'Заявка на резюме!'
        message = 'Заявка отправлена!'
        try:
            send_mass_mail(
                ((title_m, message_to_user, from_email, [to_email_user]), (title_m, message_to_header, from_email,
                                                                         [to_email_header])), fail_silently=True)
            bid = Bid(addressee=request.user, destination=destination, status=status, title=title, id_vr=id_vr)
            bid.save()
        except:
            message = 'Заявка НЕ отправлена!'
        return Response({
            'message': message
        })
