from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    nome_completo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    TIPO_UTILIZADOR_CHOICES = [
        ('CIDADAO', 'Cidadão'),
        ('FUNCIONARIO', 'Funcionário Judicial'),
        ('ADMIN', 'Administrador'),
    ]
    tipo_utilizador = models.CharField(max_length=20, choices=TIPO_UTILIZADOR_CHOICES)
    data_criacao = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo']

    groups = models.ManyToManyField('auth.Group', verbose_name='groups', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name="custom_user_set", related_query_name="user",)
    user_permissions = models.ManyToManyField('auth.Permission', verbose_name='user permissions', blank=True, help_text='Specific permissions for this user.', related_name="custom_user_set", related_query_name="user" )

    def __str__(self):
        return self.email
    

class Log(models.Model):
    utilizador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='logs')
    acao = models.CharField(max_length=255)
    data_hora = models.DateTimeField(auto_now_add=True)
    detalhes = models.TextField()
    ip = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.acao} - {self.data_hora}"

class Cidadao(models.Model):
    utilizador = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='cidadao')
    numero_bi_nuit = models.CharField(max_length=50, unique=True)
    endereco = models.TextField()
    provincia = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.numero_bi_nuit


class FuncionarioJudicial(models.Model):
    utilizador = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='funcionario')
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    nivel_acesso = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.utilizador.nome_completo} - {self.cargo}"
