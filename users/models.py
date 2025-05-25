from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from datetime import datetime, timedelta, timezone


class MyUserManager(UserManager):

    def _create_user(self, user_name, email, password, **extra_fields):
        """
        Crie e salve um usuário com o nome de usuário, e-mail e senha fornecidos.
        """
        if not user_name:
            raise ValueError('O nome de usuário fornecido deve ser definido')

        if not email:
            raise ValueError('O e-mail fornecido deve ser definido')

        email = self.normalize_email(email)
        user_name = self.model.normalize_username(user_name)
        user = self.model(user_name=user_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_name, email, password, **extra_fields)

    def create_superuser(self, user_name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('O superusuário deve ter is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('O superusuário deve ter is_superuser=True')

        return self._create_user(user_name, email, password, **extra_fields)


# class User(AbstractBaseUser, PermissionsMixin, TrackingModel):

class User(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_set',  # Specify a custom related_name
        related_query_name='custom_user'  # Specify a custom related_query_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='custom_user_set',  # Specify a custom related_name
        related_query_name='custom_user'  # Specify a custom related_query_name
    )
    """Uma classe base abstrata que implementa um modelo de usuário completo com
    permissões compatíveis com administrador.Nome de usuário e senha são necessários. Outros campos são opcionais.
    """
    # username_validator = UnicodeUsernameValidator()
    user_name = models.CharField(('user_name'), max_length=150, unique=True, help_text=(
        'Requeridos. 150 caracteres ou menos. Apenas letras, dígitos e @/./+/-/_.'),
        error_messages={
            'unique': ("Um usuário com esse nome já existe."),
    },
    )

    full_name = models.CharField(("Nome completo"), max_length=255)
    phone_number = models.CharField(("Celular"), max_length=255)
    email = models.EmailField(('email address'), blank=True, null=True, unique=True, error_messages={
        'unique': ("Um usuário com este email já existe")
    })
    administrator = models.BooleanField(("Administrador"), default=False)
    jury = models.BooleanField(("Administrador"), default=False)

    is_staff = models.BooleanField(('staff status'), default=False, help_text=(
        'Designa se o usuário pode fazer login neste site de administração.'),
    )
    is_active = models.BooleanField(('active'), default=True, help_text=(
        'Designa se este usuário deve ser tratado como ativo.'
        'Desmarque isso em vez de excluir contas.'),
    )

    date_joined = models.DateTimeField(('date joined'), default=datetime.now)
    # email_verified = models.BooleanField(_('email_verified'),default=False,
    # help_text=_('Designa se o e-mail deste usuário é verificado.'),)

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', "full_name"]

    @property
    def token(self):
        token = jwt.encode(
            {'user_name': self.user_name, 'email': self.email,
                'exp': datetime.utcnow() + timedelta(hours=24)},
            settings.SECRET_KEY, algorithm='HS256')
        return token

    def __str__(self):
        return '{}, {}'.format(self.user_name, self.email)

class Cidadao(models.Model):
    full_name = models.CharField(("Nome completo"), max_length=255)
    numero_bi_nuit = models.CharField(max_length=50, unique=True)
    endereco = models.TextField()
    provincia = models.CharField(max_length=100)
    nacionalidade = models.CharField(max_length=100, null=True)
    distrito = models.CharField(max_length=100)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.full_name
    
    def tem_registos_criminais(self):
        return self.registos_criminais.exists()


class FuncionarioJudicial(models.Model):
    utilizador = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='funcionario')
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    nivel_acesso = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.utilizador.full_name} - {self.cargo}"
