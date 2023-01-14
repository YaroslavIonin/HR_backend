from django.contrib.auth.hashers import make_password, identify_hasher
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# from back.models import Resume, Vacancy


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, full_name=None,
                     is_active=False, is_staff=None, is_admin=None, is_header_dep=None, department=None, image=None):
        if not email:
            raise ValueError('Пользователь должен иметь email')

        if not password:
            raise ValueError('Пользователь должен ввести пароль')

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.full_name = full_name
        user.is_header_dep = is_header_dep
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, full_name=None):
        user = self.create_user(email=email, password=password, full_name=full_name, is_active=True,
                                is_staff=True, is_admin=True, is_header_dep=True)
        return user

    def create_staffuser(self, email, password=None, full_name=None):
        user = self.create_user(email=email, password=password, full_name=full_name,
                                is_staff=True, is_admin=False)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255, verbose_name='Email')
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО сотрудника')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False, verbose_name='Админ')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания аккаунта')
    is_header_dep = models.BooleanField(default=False, verbose_name='Глава департамента')
    department = models.ForeignKey('Department', on_delete=models.RESTRICT, blank=True, null=True, verbose_name='Департамент')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True, null=True, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.full_name:
            return self.full_name
        return 'Введите ФИО'

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        try:
            self.is_staff = self.is_admin
        except AttributeError:
            self.is_staff = False
            self.is_admin = False
        try:
           _alg_ = identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        if self.is_admin:
            self.is_header_dep = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']


class Department(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название департамента')
    description = models.TextField(max_length=500, verbose_name='Описание департамента', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'
        ordering = ['name']


class Bid(models.Model):
    addressee = models.ForeignKey(User, related_name='bids', verbose_name='От кого', on_delete=models.CASCADE)
    destination = models.ForeignKey(User, verbose_name='Кому(поле id)', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Заявка на вакансию:', blank=True)
    status = models.CharField(max_length=50, choices=[
        ('1', 'Вакансия'),
        ('2', 'Резюме')
    ], default=None, verbose_name='Заявка на что')
    data_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата редактирования')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-data_created']

